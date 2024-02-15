from base64 import b64encode
from typing import Dict, Any, List, Type
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

from modules.database.dbconnector import *
from modules.models.data_model import *
from modules.models.db_class import *
from modules.test.test_main import *
from modules.analize.check_symbols import *
from modules.account.jwt_impl import *
from passlib.context import CryptContext
import json
import os
import shutil
import random
import string
import datetime


with open("config.json", 'r') as config_file:
    config_data = json.load(config_file)


app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config_data['origins'],
    allow_credentials=config_data['credentials'],
    allow_methods=config_data['methods'],
    allow_headers=config_data['headers']
)

init_test_db_data()


@app.get("/", status_code=404)
async def read_root() -> HTMLResponse:
    html_content: str = "Error 404. Here is no page"
    return HTMLResponse(content=html_content, status_code=404)


@app.post("/register", response_model=UserResponseModel)
def create_user(user: RegisterRequestModel):
    hashed_password = pwd_context.hash(user.password)
    user_id = create_user_db(username=user.username, password=hashed_password, role='student', study_group_name=user.group_name)
    payload = {"sub": user.username, "role": 'student'}
    access_token = create_access_token(data=payload)
    response = {
        "id": user_id,
        "username": user.username,
        'role': 'student',
        "access_token": access_token
    }
    return response


@app.post("/login", response_model=UserResponseModel)
def login_for_access_token(login_request: LoginRequestModel):
    user = get_user_db(login_request.username)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"}
        )
    elif not pwd_context.verify(login_request.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    payload = {"sub": user.username, "role": user.role}
    access_token = create_access_token(data=payload)
    response = {
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "access_token": access_token
    }
    return response


@app.get("/user_dashboard", response_model=UserDashboardModel)
def get_user_dashboard(current_user: User = Depends(get_current_user)):
    print(current_user)
    role = Roles[current_user.role]
    if role != Roles.student:
        raise HTTPException(
            status_code=403,
            detail="Access Denied",
            headers={"WWW-Authenticate": "Bearer"}
        )
    response = UserDashboardModel(
        id=current_user.id,
        username=current_user.username
    )
    return response


@app.get("/teacher_dashboard", response_model=TeacherDashboardModel)
def get_teacher_dashboard(current_user: User = Depends(get_current_user)):
    role = Roles[current_user.role]
    if role != Roles.teacher:
        raise HTTPException(
            status_code=403,
            detail="Access Denied",
            headers={"WWW-Authenticate": "Bearer"}
        )
    response = TeacherDashboardModel(
        id=current_user.id,
        username=current_user.username
    )
    return response


@app.get(
    "/tasks",
    response_class=JSONResponse,
    responses={
        200: {
            "description": "Возвращает словарь, где ключи — это ID тестов, а значения — их названия.",
            "content": {
                "application/json": {
                    "example": {"1": "Работа с переменными", "2": "Работа с алгебраическими выражениями"}
                }
            }
        }
    }
)
async def get_tasks() -> Dict[str, str]:
    content: Dict[str, str] = {str(test.id): test.description for test in await get_all_tests()}
    return content


@app.get("/task/{test_id}")
async def get_task_info(test_id: int, current_user: User = Depends(get_current_user)) -> TestInfoModel:
    test_info = await get_test_by_id(test_id)
    results = get_user_test_attempts(user_id=current_user.id, test_id=test_id)
    response = TestInfoModel(
         id=test_info.id,
         description=test_info.description,
         attempts=results
    )
    return response


@app.get("/full_test_info/{test_id}")
async def get_task_info(test_id: int, current_user: User = Depends(get_current_user)) -> TestModel:
    role = Roles[current_user.role]
    if role != Roles.teacher:
        raise HTTPException(
            status_code=403,
            detail="Access Denied",
            headers={"WWW-Authenticate": "Bearer"}
        )
    test_info = await get_test_by_id(test_id)

    functions = []
    for function in test_info.functions:
        test_cases = []
        input_data = []
        sorted_data = sorted(function.datas, key=lambda x: x.data_pose if x.data_pose != -1 else float('inf'))

        for data in sorted_data:
            if data.data_pose != -1:
                input_data.append(data.data)
            else:
                test_cases.append(TestCaseModel(input=input_data, output=data.data))
                input_data = []

        formulas = [FormulaModel(id=formula.id, formula=formula.formula) for formula in function.formulas]

        #linked_formulas = [LinkedFormulaModel(
        #    id=linked_formula.id,
        #    description=linked_formula.description,
        #    formula_ids=linked_formula.formula_ids)
        #    for linked_formula in function.linked_formulas
        #]

        functions.append(FunctionModel(
            name=function.func_name,
            test_cases=test_cases,
            formulas=formulas,
        #    linked_formulas=linked_formulas
        ))

    constructions = [ConstructionModel(name=construction.name, state=construction.state) for construction in
                     test_info.constructions] if test_info.constructions else None
    length_checks = [CodeLengthModel(symbols=length.symbols, rows=length.rows) for length in
                     test_info.lengths] if test_info.lengths else None

    response = TestModel(
        task_text=test_info.description,
        functions=functions,
        constructions=constructions,
        length_checks=length_checks
    )
    return response


@app.post("/check/{test_id}")
async def check_task(test_id: int, item: CheckModel, current_user: User = Depends(get_current_user)) -> JSONResponse:
    unique_id: str = str(test_id) + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(7)) \
                     + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    os.mkdir(f"trash/{unique_id}")
    file: str = item.file
    test: Type[Test] = await get_test_by_id(test_id)
    filename: str = "test_" + str(test_id) + ''.join(random.choice(string.ascii_lowercase + string.digits)
                                                     for _ in range(3)) + datetime.datetime.now().strftime('%Y%m%d%H%M%S') \
                    + ".py"
    write_file(filename, file, unique_id)
    checks: Dict[str, List[Any]] = run_test(filename, test.functions, unique_id)
    lengths: List[Dict[str, int | bool | None]] = [
        check_symbols(filename, length, unique_id) for length in test.lengths
    ]
    with open(f"trash/{unique_id}/output.xml", "rb") as export_file:
        output: str = b64encode(export_file.read()).decode('utf-8')
    with open(f"trash/{unique_id}/errors.txt", "rb") as export_file:
        error: str = b64encode(export_file.read()).decode('utf-8')
    for directory in [".pytest_cache", "__pycache__", f"trash/{unique_id}"]:
        try:
            shutil.rmtree(directory)
        except Exception as e:
            print(e.__str__())
    response = {
        "test_results": output,
        "test_errors": error,
        "test_passed": checks,
        "lengths": lengths
    }
    attempt_id = await save_test_result(
        user_id=current_user.id,
        test_id=test_id,
        test_results=response
    )
    response['attempt_id'] = attempt_id
    return JSONResponse(content=jsonable_encoder(response))


@app.post("/newtask", status_code=201)
async def insert_task(item: QueryData) -> JSONResponse:
    try:
        answer: str = await insert_vals(item.lab_task)
        response = {
            "status": answer
        }
        return JSONResponse(content=response)
    except Exception as ex:
        response = {
            "status": ex.__str__()
        }
        return JSONResponse(content=response, status_code=400)


@app.get("/get_students_groups", response_model=List[StudyGroupResponseModel])
async def get_students_groups():
    return get_students_groups_db()


@app.get("/{smth}", status_code=404)
async def not_found(smth: str) -> HTMLResponse:
    return HTMLResponse(content=f"Error 404, {smth} is not valid gateway", status_code=404)
