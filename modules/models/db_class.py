import enum
from datetime import datetime
from typing import List
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped
from sqlalchemy import Integer, String, ForeignKey, Text, DateTime, Enum, JSON
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    pass


class Test(Base):
    __tablename__ = "Test"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column()
    functions: Mapped[List["Function"]] = relationship(back_populates="test", cascade="all, delete-orphan")
    lengths: Mapped[List["CodeLength"]] = relationship(back_populates="test", cascade="all, delete-orphan")
    constructions: Mapped[List["Construction"]] = relationship(back_populates="test", cascade="all, delete-orphan")
    study_group_tests: Mapped[List["StudyGroupTest"]] = relationship("StudyGroupTest", back_populates="test")


class Function(Base):
    __tablename__ = "Function"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    func_name: Mapped[str] = mapped_column(nullable=False)
    testid: Mapped[int] = mapped_column(ForeignKey("Test.id"))
    test: Mapped["Test"] = relationship(back_populates="functions")
    datas: Mapped[List["Data"]] = relationship(back_populates="function_t", cascade="all, delete-orphan")
    formulas: Mapped[List["Formula"]] = relationship(back_populates="function_t", cascade="all, delete-orphan")


class Data(Base):
    __tablename__ = "Data"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    data_pose: Mapped[int] = mapped_column()
    data: Mapped[str] = mapped_column(nullable=False)
    functionid: Mapped[int] = mapped_column(ForeignKey("Function.id"))
    function_t: Mapped["Function"] = relationship(back_populates="datas")


class Formula(Base):
    __tablename__ = "Formula"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    num: Mapped[int] = mapped_column(nullable=False)
    formula: Mapped[str] = mapped_column(nullable=False)
    functionid: Mapped[str] = mapped_column(ForeignKey("Function.id"))
    function_t: Mapped["Function"] = relationship(back_populates="formulas")


class CodeLength(Base):
    __tablename__ = "CodeLength"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symbols: Mapped[int] = mapped_column(nullable=True)
    rows: Mapped[int] = mapped_column(nullable=True)
    testid: Mapped[int] = mapped_column(ForeignKey("Test.id"))
    test: Mapped["Test"] = relationship(back_populates="lengths")


class Construction(Base):
    __tablename__ = "Construction"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    state: Mapped[bool] = mapped_column(nullable=False)
    testid: Mapped[int] = mapped_column(ForeignKey("Test.id"))
    test: Mapped["Test"] = relationship(back_populates="constructions")


class StudyGroup(Base):
    __tablename__ = "StudyGroup"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    students: Mapped[List["User"]] = relationship("User", back_populates="study_group")
    study_group_tests: Mapped[List["StudyGroupTest"]] = relationship("StudyGroupTest", back_populates="study_group")


class StudyGroupTest(Base):
    __tablename__ = 'study_group_test'
    study_group_id: Mapped[int] = mapped_column(Integer, ForeignKey('StudyGroup.id'), primary_key=True)
    test_id: Mapped[int] = mapped_column(Integer, ForeignKey('Test.id'), primary_key=True)
    assignment_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    deadline: Mapped[datetime] = mapped_column(DateTime)
    study_group: Mapped[StudyGroup] = relationship("StudyGroup", back_populates="study_group_tests")
    test: Mapped[Test] = relationship("Test", back_populates="study_group_tests")


class Roles(enum.Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"


class User(Base):
    __tablename__ = "User"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[Roles] = mapped_column(Enum(Roles), nullable=False)
    study_group_id: Mapped[int] = mapped_column(Integer, ForeignKey('StudyGroup.id'), nullable=True)
    study_group: Mapped[StudyGroup] = relationship("StudyGroup", back_populates="students")
    test_results: Mapped[List["TestResult"]] = relationship("TestResult", back_populates="user")


class TestResult(Base):
    __tablename__ = "TestResult"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('User.id'), nullable=False)
    test_id: Mapped[int] = mapped_column(Integer, ForeignKey('Test.id'), nullable=False)
    test_results: Mapped[dict] = mapped_column(JSON, nullable=False)
    #test_results: Mapped[str] = mapped_column(Text, nullable=False)
    #test_errors: Mapped[str] = mapped_column(Text, nullable=False)
    #test_passed: Mapped[str] = mapped_column(Text, nullable=False)
    #lengths: Mapped[str] = mapped_column(Text, nullable=False)
    user: Mapped[User] = relationship("User", back_populates="test_results")
    test: Mapped[Test] = relationship("Test")


__all__ = ["Base", "Test", "Formula", "Data", "Function", "Construction", "CodeLength", "StudyGroup", "Roles", "StudyGroupTest", "User", "TestResult"]
