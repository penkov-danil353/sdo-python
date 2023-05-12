from base64 import b64encode
from typing import Dict, Any, List, Type
from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from modules.database.dbconnector import *
from modules.models.data_model import QueryData
from modules.models.db_class import *
from modules.test.test_main import *
import os
import shutil


def remove(folder: str) -> None:
    for filename in os.listdir(folder):
        file_path: str = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


app = FastAPI()


@app.get("/")
def read_root() -> HTMLResponse:
    html_content: str = "Nothing to see here"
    return HTMLResponse(content=html_content, status_code=404)


@app.get("/tasks")
def get_tasks() -> JSONResponse:
    content: Dict[str, str] = {str(test.id): test.description for test in get_all_tests()}
    return JSONResponse(content=content)


@app.get("/check/{id}")
def check_task(id, body=Body()) -> JSONResponse:
    file: str = body["file"]
    test: Type[Test] = get_test_by_id(id)
    filename: str = "test_unit.py"
    write_file(filename, file)
    functions = []
    for function in test.functions:
        function.test = None
        functions.append(function)
    checks: Dict[str, List[Any]] = run_test(filename, functions)
    with open("./trash/output.xml", "rb") as export_file:
        output: str = b64encode(export_file.read()).decode('utf-8')
    with open("./trash/errors.txt", "rb") as export_file:
        error: str = b64encode(export_file.read()).decode('utf-8')
    try:
        shutil.rmtree("./.pytest_cache")
    except Exception:
        pass
    remove("./trash")
    return JSONResponse(content=jsonable_encoder(
        {"test_results": output, "test_errors": error, "test_passed": checks}))


@app.post("/newtask")
def insert_task(item: QueryData) -> JSONResponse:
    return JSONResponse(content={"error_code": -1})
