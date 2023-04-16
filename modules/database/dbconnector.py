from typing import Type

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from modules.models import *

import os

sqlite_database = os.environ.get("db_con", "sqlite:///database/test.db")
engine = create_engine(sqlite_database, echo=True)
Base.metadata.create_all(bind=engine)


def add_data(*args: Test):
    with Session(autoflush=False, bind=engine) as db:
        for test_val in args:
            db.add(test_val)
        db.commit()


def get_all_tests():
    with Session(autoflush=False, bind=engine) as db:
        tests = db.query(Test).all()
        return tests


def get_test_by_id(id_val: int):
    with Session(autoflush=False, bind=engine) as db:
        test_val: Type[Test] = db.query(Test).filter(Test.id == id_val).first()
        for function in test_val.functions:
            function.func_name
            function.datas
            function.formulas
        return test_val
