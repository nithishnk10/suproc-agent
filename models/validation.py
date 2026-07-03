from typing import List
from pydantic import BaseModel


class ValidationResult(BaseModel):
    passed: bool
    errors: List[str]