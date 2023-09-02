from typing import List, Dict, Any

from pydantic import BaseModel, Field


class CheckResult(BaseModel):
    test_results: str = Field(default=None, description="Unit test results file deciphered by base64 encoding")
    test_errors: str = Field(default=None, description="SLP check results file deciphered by base64 encoding")
    test_passed: Dict[str, List[Any]] = Field(default=None, description="Tests data")
    lengths: List[Dict[str, int | bool | None]] = Field(default=None, description="Length test data")


__all__ = ["CheckResult"]
