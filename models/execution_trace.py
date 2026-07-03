from typing import List
from pydantic import BaseModel


class ExecutionTrace(BaseModel):
    steps: List[str]