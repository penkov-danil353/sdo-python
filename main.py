from base64 import b64encode
from typing import Dict, List
from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from modules.database.dbconnector import *
from modules.models.db_class import *
from modules.test.__main import *
import os
import shutil


def remove(folder: str):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


app = FastAPI()


@app.get("/", status_code=404)
def read_root():
    html_content = "Nothing to see here"
    return HTMLResponse(content=html_content, status_code=404)


@app.get("/tasks")
def get_tasks():
    content: Dict[str, str] = {str(test.id): test.description for test in get_all_tests()}
    return JSONResponse(content=content)


@app.get("/check/{id}")
def check_task(id, body=Body()) -> JSONResponse:
    file = body["file"]
    test: Test = get_test_by_id(id)
    filename = "test_unit.py"
    write_file(filename, file)
    functions = []
    for function in test.functions:
        function.test = None
        functions.append(function)
    checks: Dict[str, list] = run_test(filename, functions)
    with open("./trash/output.xml", "rb") as file:
        output = b64encode(file.read()).decode('utf-8')
    with open("./trash/errors.txt", "rb") as file:
        error = b64encode(file.read()).decode('utf-8')
    try:
        shutil.rmtree("./.pytest_cache")
    except Exception:
        pass
    remove("./trash")
    return JSONResponse(content=jsonable_encoder(
        {"test_results": output, "test_errors": error, "test_passed": checks}))


@app.post("/newtask")
def insert_task(body=Body()) -> JSONResponse:
    return JSONResponse(content={"error_code": -1})
