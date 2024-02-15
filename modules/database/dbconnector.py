from typing import Type, List, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

from passlib.context import CryptContext

from modules.models.data_model import TestResultModel
from modules.models.db_class import *
from modules.models.data_model import *

import os

sqlite_database = os.environ.get("DB_CON")
engine = create_engine(sqlite_database, echo=True)
Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user_db(username, password, role, study_group_name=None) -> int:
    role_enum = Roles[role.lower()]
    study_group_id = get_or_create_study_group(name=study_group_name)
    user = User(username=username, password=password, role=role_enum, study_group_id=study_group_id)
    with Session(autoflush=False, bind=engine) as db:
        db.add(user)
        db.flush()
        user_id = user.id
        db.commit()
    return user_id


def get_user_db(username: str) -> Optional[UserModel]:
    with Session(autoflush=False, bind=engine) as db:
        user_record = db.query(User).filter(User.username == username).first()

        if not user_record:
            return None

        user = UserModel(
            id=user_record.id,
            username=user_record.username,
            password=user_record.password,
            role=user_record.role.name
        )
        return user


async def save_test_result(user_id: int, test_id: int, test_results: dict) -> int:
    record = TestResult(user_id=user_id, test_id=test_id, test_results=test_results)
    with Session(autoflush=False, bind=engine) as db:
        db.add(record)
        db.flush()
        attempt_id = record.id
        db.commit()
    return attempt_id


def get_or_create_study_group(name: str) -> int:
    with Session(autoflush=False, bind=engine) as db:
        try:
            study_group = db.query(StudyGroup).filter(StudyGroup.name == name).one()
        except NoResultFound:
            study_group = StudyGroup(name=name)
            db.add(study_group)
            db.flush()
            db.commit()
        return study_group.id


def get_students_groups_db() -> List:
    with Session(autoflush=False, bind=engine) as db:
        study_groups = db.query(StudyGroup).all()
        return study_groups



async def add_data(*args: Test) -> None:
    with Session(autoflush=False, bind=engine) as db:
        for test_val in args:
            db.add(test_val)
        db.commit()


async def get_all_tests() -> List[Type[Test]]:
    with Session(autoflush=False, bind=engine) as db:
        tests: List[Type[Test]] = db.query(Test).all()
        return tests


def get_user_test_attempts(user_id: int, test_id: int) -> List[TestResultModel]:
    with Session(autoflush=False, bind=engine) as db:
        result = db.execute(
            select(TestResult).where(
                TestResult.user_id == user_id,
                TestResult.test_id == test_id
            )
        )
        test_results = result.scalars().all()
        return [
            TestResultModel(
                id=test_result.id,
                user_id=test_result.user_id,
                test_id=test_result.test_id,
                test_results=test_result.test_results
            ) for test_result in test_results
        ]


async def get_test_by_id(id_val: int) -> Type[Test]:
    with Session(autoflush=False, bind=engine) as db:
        test_val: Type[Test] = db.query(Test).filter(Test.id == id_val).first()
        for function in test_val.functions:
            function.func_name
            function.datas
            function.formulas
        test_val.lengths
        test_val.constructions
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


def init_test_db_data() -> None:
    if not get_user_db('user'):
        hashed_password = pwd_context.hash('user')
        create_user_db(username='user', password=hashed_password, role='student', study_group_name='222-330')
    if not get_user_db('admin'):
        hashed_password = pwd_context.hash('admin')
        create_user_db(username='admin', password=hashed_password, role='teacher')


__all__ = ["init_test_db_data", "get_all_tests", "get_test_by_id", "insert_vals", "create_user_db", "get_user_db", "get_or_create_study_group", "get_students_groups_db", "save_test_result", "get_user_test_attempts"]
