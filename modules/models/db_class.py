from __future__ import annotations
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
    functionid: Mapped[int] = mapped_column(ForeignKey("Function.id"))
    function_t: Mapped["Function"] = relationship(back_populates="formulas")
