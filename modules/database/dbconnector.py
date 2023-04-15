from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from modules.models import *

sqlite_database = "sqlite:///test.db"
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
        test_val = db.query(Test).filter(Test.id == id_val).first()
        return test_val


if __name__ == "__main__":
    test: Test = Test(description="1", functions=[Function(
        func_name="compute_binom",
        datas=[Data(data_pose=0, data="2"), Data(data_pose=1, data="2"), Data(data_pose=-1, data="1")],
        formulas=[Formula(num=0, formula="z = n - k")]
    )])
    test1: Test = Test(description="1", functions=[Function(
        func_name="factorial",
        datas=[Data(data_pose=0, data="5"), Data(data_pose=-1, data="120")]
    )])
    add_data(test, test1)
    for test in get_all_tests():
        print(get_test_by_id(test.id))
