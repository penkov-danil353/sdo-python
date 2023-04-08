from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI()


@app.get("/", status_code=404)
def read_root():
    html_content = "Nothing to see here"
    return HTMLResponse(content=html_content)


@app.get("/tasks")
def get_tasks():
    return JSONResponse(content={1: "void"})


@app.get("/check/{id}")
def check_task(task_id: int, body=Body()):
    return JSONResponse(content={"test_results": "void", "test_errors": "void", "test_passed": ["void", "void"]})


@app.post("/newtask")
def insert_task(body: Body = Body()):
    return JSONResponse(content={"error_code": -1})
