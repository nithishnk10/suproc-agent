from typing import List
from pydantic import BaseModel


class DatasetCapability(BaseModel):
    available: List[str]
    unavailable: List[str]