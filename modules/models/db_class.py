from typing import List
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped
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


__all__ = ["Base", "Test", "Formula", "Data", "Function", "Construction", "CodeLength"]
