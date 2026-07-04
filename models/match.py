from typing import Dict, List
from pydantic import BaseModel


class Match(BaseModel):
    entity_id: str
    entity_name: str
    entity_type: str
    location: str

    score: float
    breakdown: Dict[str, float]
    evidence: List[str] = []