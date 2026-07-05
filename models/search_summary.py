from typing import Optional
from pydantic import BaseModel


class SearchSummary(BaseModel):
    total_entities: int
    location_matches: int
    match1: int
    match2: int | None
    match3: int | None
    final_matches: int