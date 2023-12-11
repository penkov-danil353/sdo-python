from typing import List, Any
from .db_class import TestResult
from pydantic import BaseModel, Field
from typing import Literal


class TestCaseModel(BaseModel):
    input: List[Any] | None = Field(default=None, description="Function input data")
    output: Any | None = Field(default=None, description="Function output data")


class FormulaModel(BaseModel):
    id: str = Field(description="Formula id for linking")
    description: str | None = Field(default=None, title="Description of function")
    formula: str = Field(description="Formula")


class LinkedFormulaModel(BaseModel):
    id: str | None = Field(default=None, description="Linked formula id")
    description: str | None = Field(default=None, title="Description of linked formula")
    formula_ids: List[str]


class FunctionModel(BaseModel):
    name: str = Field(description="Name of tested function")
    test_cases: List[TestCaseModel] = Field(description="Data used for validation")
    formulas: List[FormulaModel] | None = Field(description="Formulas test cases")
    linked_formulas: List[LinkedFormulaModel] | None = Field(default=None, description="Formula linkage")


class ConstructionModel(BaseModel):
    name: str = Field(description="Construction name like \"for\" and etc")
    state: bool = Field(description="True for checking of construction presence and false for not")


class CodeLengthModel(BaseModel):
    symbols: int | None = Field(default=None, description="File length in symbols except whitespace symbols. "
                                                          "None is for disabling check")
    rows: int | None = Field(default=None, description="File length in rows. None for disabling")


class TestModel(BaseModel):
    task_text: str = Field(description="Task description", max_length=1024)
    functions: List[FunctionModel] | None = Field(default=None, description="Test case for function testing")
    constructions: List[ConstructionModel] | None = Field(default=None, description="List of constructions for check")
    length_checks: List[CodeLengthModel] | None = Field(default=None, description="Code length checks")


class TestResultModel(BaseModel):
    id: int = Field(description="Attempt ID")
    user_id: int = Field(description="User ID")
    test_id: int = Field(description="Test ID")
    test_results: dict = Field(description="Test result structure")

    class Config:
        orm_mode = True
        from_attributes = True


class TestInfoModel(BaseModel):
    id: int = Field(description="Test ID")
    description: str = Field(description="Test description", max_length=1024)
    attempts: List[TestResultModel]


class QueryData(BaseModel):
    lab_task: TestModel = Field(description="Test task")


class CheckModel(BaseModel):
    file: str = Field(description="File for checking")


class UserModel(BaseModel):
    id: int = Field(description="User ID")
    username: str = Field(description="User login")
    password: str = Field(description="User password")
    role: Literal["admin", "teacher", "student"] = Field(description="User role")


class LoginRequestModel(BaseModel):
    username: str = Field(description="User login")
    password: str = Field(description="User password")


class RegisterRequestModel(BaseModel):
    username: str = Field(description="User login")
    password: str = Field(description="User password")
    group_id: int = Field(description="Students group ID")


class UserResponseModel(BaseModel):
    id: int = Field(description="User ID")
    username: str = Field(description="User login")
    role: Literal["admin", "teacher", "student"] = Field(description="User role")
    access_token: str = Field(description="JWT token")


class UserDashboardModel(BaseModel):
    id: int = Field(description="User ID")
    username: str = Field(description="User login")


class TeacherDashboardModel(BaseModel):
    id: int = Field(description="User ID")
    username: str = Field(description="User login")


class StudyGroupRequestModel(BaseModel):
    name: str = Field(description="Group name")


class StudyGroupResponseModel(BaseModel):
    id: int = Field(description="Group ID")
    name: str = Field(description="Group name")


__all__ = ["TestModel", "TestInfoModel", "CodeLengthModel", "ConstructionModel", "FunctionModel", "FormulaModel", "LinkedFormulaModel",
           "TestCaseModel", "QueryData", "CheckModel",
           "UserModel", "UserResponseModel", "UserDashboardModel", "RegisterRequestModel", "LoginRequestModel", "TeacherDashboardModel",
           "StudyGroupRequestModel", "StudyGroupResponseModel"]
