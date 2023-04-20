from base64 import b64encode
from typing import Dict, Any, List, Type
from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from modules.database.dbconnector import *
from modules.models.db_class import *
from modules.test.test_main import *
import os
import shutil


def remove(folder: str) -> None:
    """
    Удаляет содержимое папки
    :param folder: путь до папки, которую необходимо очистить
    :return: None
    """
    for filename in os.listdir(folder):
        file_path: str = os.path.join(folder, filename)  # получает путь до конкретного содержимого
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):  # проверяет файл или ссылка указанный путь
                os.unlink(file_path)
            elif os.path.isdir(file_path):   # проверяет, является ли путь папкой
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


# точка входа
app = FastAPI()


@app.get("/")
def read_root() -> HTMLResponse:
    """
    Затычка для любопытных исследователей
    :return: Простенькую html страницу с текстом и кодом 404
    """
    html_content: str = "Nothing to see here"
    return HTMLResponse(content=html_content, status_code=404)


@app.get("/tasks")
def get_tasks() -> JSONResponse:
    """
    Первый эндпоинт. Позволяет получать список заданий
    :return: Json документ состоящий из id заданий и соответствующих описаний
    """
    content: Dict[str, str] = {str(test.id): test.description for test in get_all_tests()}
    # Просто преобразуем данные в нужную нам форму, т.к. нода бд возвращает модели
    return JSONResponse(content=content)


@app.get("/check/{id}")
def check_task(id, body=Body()) -> JSONResponse:
    """
    Магия. Шучу. Тут начинается эндпоинт проверки заданий. Ничего сложного. Просто прилетает запрос
    содержащий в своем теле зашифрованный в base64 файл с указанным в строке запроса id задания
    :param id: Собственно id задания
    :param body: Тело запроса
    :return: Json документ, содержащий информацию по выполненным проверкам
    """
    file: str = body["file"]  # получение файла из тела запроса
    test: Type[Test] = get_test_by_id(id)  # получение задания из БД по его id
    filename: str = "test_unit.py"
    write_file(filename, file)  # создание экземпляра задания на сервере
    functions = []
    for function in test.functions:
        function.test = None
        functions.append(function)
    checks: Dict[str, List[Any]] = run_test(filename, functions)  # Непосредственно проверка кода
    with open("./trash/output.xml", "rb") as export_file:  # Чтение из файла и шифрование в base64
        output: str = b64encode(export_file.read()).decode('utf-8')
    with open("./trash/errors.txt", "rb") as export_file:  # Чтение из файла и шифрование в base64
        error: str = b64encode(export_file.read()).decode('utf-8')
    try:
        shutil.rmtree("./.pytest_cache")  # Очистка кэша тестов
    except Exception:
        pass
    remove("./trash")   # очистка тестовой директории
    return JSONResponse(content=jsonable_encoder(
        {"test_results": output, "test_errors": error, "test_passed": checks}))


@app.post("/newtask")
def insert_task(body=Body()) -> JSONResponse:
    return JSONResponse(content={"error_code": -1})
