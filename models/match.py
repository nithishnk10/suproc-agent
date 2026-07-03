from typing import Dict
from pydantic import BaseModel


class Match(BaseModel):
    supplier_id: str
    supplier_name: str
    score: float
    breakdown: Dict[str, float]