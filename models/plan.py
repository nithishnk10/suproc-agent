from typing import List
from pydantic import BaseModel


class ExecutionPlan(BaseModel):
    steps: List[str]