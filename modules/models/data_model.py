from typing import List, Type, Any

from pydantic import BaseModel, Field


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
    constructions: List[ConstructionModel] | None = Field(default=None,
                                                          description="List of constructions for check")
    length_checks: List[CodeLengthModel] | None = Field(default=None, description="Code length checks")


class QueryData(BaseModel):
    lab_task: TestModel = Field(description="Test task")
