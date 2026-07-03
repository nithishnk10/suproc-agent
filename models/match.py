from typing import Dict, List
from pydantic import BaseModel

class Match(BaseModel):
    supplier_id: str
    supplier_name: str
    score: float
    breakdown: Dict[str, float]
    evidence: List[str] = []