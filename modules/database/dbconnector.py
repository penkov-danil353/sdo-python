from typing import Type, List

from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from modules.models.db_class import *

import os

sqlite_database = os.environ.get("DB_CON", "sqlite:///database/test.db")
engine = create_engine(sqlite_database, echo=True)
Base.metadata.create_all(bind=engine)


def add_data(*args: Test) -> None:
    with Session(autoflush=False, bind=engine) as db:
        for test_val in args:
            db.add(test_val)
        db.commit()


def get_all_tests() -> List[Type[Test]]:
    with Session(autoflush=False, bind=engine) as db:
        tests: List[Type[Test]] = db.query(Test).all()
        return tests


def get_test_by_id(id_val: int) -> Type[Test]:
    with Session(autoflush=False, bind=engine) as db:
        test_val: Type[Test] = db.query(Test).filter(Test.id == id_val).first()
        for function in test_val.functions:
            function.func_name
            function.datas
            function.formulas
        return test_val


__all__ = ["get_all_tests", "get_test_by_id", "add_data"]
