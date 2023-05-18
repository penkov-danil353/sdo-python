from base64 import b64encode
from typing import Dict, Any, List, Type
from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from modules.database.dbconnector import *
from modules.models.data_model import QueryData
from modules.models.db_class import *
from modules.test.test_main import *
from modules.analize.check_symbols import *
import json
import os
import shutil
import random
import string
import datetime


with open("config.json", 'r') as config_file:
    config_data = json.load(config_file)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config_data['origins'],
    allow_credentials=config_data['credentials'],
    allow_methods=config_data['methods'],
    allow_headers=config_data['headers']
)


@app.get("/")
async def read_root() -> HTMLResponse:
    html_content: str = "Nothing to see here"
    return HTMLResponse(content=html_content, status_code=404)


@app.get("/tasks")
async def get_tasks() -> JSONResponse:
    content: Dict[str, str] = {str(test.id): test.description for test in await get_all_tests()}
    return JSONResponse(content=content)


@app.post("/check/{id}")
async def check_task(id, body=Body()) -> JSONResponse:
    unique_id: str = str(id) + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(7))\
                     + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    os.mkdir(f"./trash/{unique_id}")
    file: str = body["file"]
    test: Type[Test] = await get_test_by_id(id)
    filename: str = "test_unit.py"
    write_file(filename, file, unique_id)
    checks: Dict[str, List[Any]] = run_test(filename, test.functions, unique_id)
    lengths: List[Dict[str, int | bool | None]] = [
        check_symbols(filename, length, unique_id) for length in test.lengths
    ]
    with open(f"./trash/{unique_id}/output.xml", "rb") as export_file:
        output: str = b64encode(export_file.read()).decode('utf-8')
    with open(f"./trash/{unique_id}/errors.txt", "rb") as export_file:
        error: str = b64encode(export_file.read()).decode('utf-8')
    for directory in ["./.pytest_cache", "./__pycache__", f"./trash/{unique_id}"]:
        try:
            shutil.rmtree(directory)
        except Exception as e:
            print(e.__str__())
    return JSONResponse(content=jsonable_encoder(
        {"test_results": output, "test_errors": error, "test_passed": checks, "lengths": lengths}))


@app.post("/newtask")
async def insert_task(item: QueryData) -> JSONResponse:
    try:
        answer: str = await insert_vals(item.lab_task)
        return JSONResponse(content={"status": answer})
    except Exception as ex:
        return JSONResponse(content={"status": ex.__str__()}, status_code=400)
