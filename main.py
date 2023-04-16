from typing import Dict
from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from modules.database.dbconnector import *
from modules.models.db_class import *

app = FastAPI()


@app.get("/", status_code=404)
def read_root():
    html_content = "Nothing to see here"
    return HTMLResponse(content=html_content)


@app.get("/tasks")
def get_tasks():
    tests: List[Test] = get_all_tests()
    content: Dict[str, str] = {}
    for test in tests:
        content[test.id.__str__()] = test.description
    return JSONResponse(content=content)


@app.get("/check/{id}")
def check_task(task_id: int, body=Body()):
    test: Test = get_test_by_id(task_id)
    return JSONResponse(content={"test_results": "void", "test_errors": "void", "test_passed": ["void", "void"]})


@app.post("/newtask")
def insert_task(body: Body = Body()):
    return JSONResponse(content={"error_code": -1})
