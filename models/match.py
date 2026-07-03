from typing import Dict, List
from pydantic import BaseModel

class Match(BaseModel):
    supplier_id: str
    supplier_name: str
    state: str
    score: float
    breakdown: Dict[str, float]
    evidence: List[str] = []