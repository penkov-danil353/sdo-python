from typing import Type, List

from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from modules.models.db_class import *
from modules.models.data_model import *

import os

sleep(60)
sqlite_database = os.environ.get("DB_CON", "sqlite:///database/test.db")
engine = create_engine(sqlite_database, echo=True)
Base.metadata.create_all(bind=engine)


async def add_data(*args: Test) -> None:
    with Session(autoflush=False, bind=engine) as db:
        for test_val in args:
            db.add(test_val)
        db.commit()


async def get_all_tests() -> List[Type[Test]]:
    with Session(autoflush=False, bind=engine) as db:
        tests: List[Type[Test]] = db.query(Test).all()
        return tests


async def get_test_by_id(id_val: int) -> Type[Test]:
    with Session(autoflush=False, bind=engine) as db:
        test_val: Type[Test] = db.query(Test).filter(Test.id == id_val).first()
        for function in test_val.functions:
            function.func_name
            function.datas
            function.formulas
        return test_val


async def insert_vals(data: TestModel) -> str:
    test: Test = Test(description=data.task_text)
    if data.constructions is not None:
        test.constructions = [Construction(name=construction.name, state=construction.state)
                              for construction in data.constructions]
    if data.length_checks is not None:
        test.lengths = [CodeLength(symbols=length.symbols, rows=length.rows) for length in data.length_checks]
    if data.functions is not None:
        functions: List[Function] = []
        for function in data.functions:
            testcases: List[Data] = []
            for testcase in function.test_cases:
                testcases += [Data(data_pose=i, data=str(testcase.input[i])) for i in range(len(testcase.input))]
                testcases.append(Data(data_pose=-1, data=str(testcase.output)))
            formulas: List[Formula] | None = None
            if function.formulas is not None:
                formulas = [Formula(num=0, formula=formula.formula) for formula in function.formulas]
                if function.linked_formulas is not None:
                    for linked_formulas in function.linked_formulas:
                        for id_ in linked_formulas.formula_ids:
                            i: int = 0
                            j: int = 0
                            for formula in function.formulas:
                                if formula.id == id_:
                                    formulas[i].num = j
                                    j += 1
                                i += 1
            functions.append(Function(func_name=function.name, datas=testcases))
            if formulas is not None:
                functions[-1].formulas = formulas
        test.functions = functions
    await add_data(test)
    return "success"


__all__ = ["get_all_tests", "get_test_by_id", "insert_vals"]
