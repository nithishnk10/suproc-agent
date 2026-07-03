from typing import List, Optional
from pydantic import BaseModel, Field


class HardConstraints(BaseModel):
    locations: List[str] = Field(default_factory=list)
    product_category: Optional[str] = None
    certifications: List[str] = Field(default_factory=list)
    minimum_capacity: Optional[int] = None
    maximum_delivery_days: Optional[int] = None


class Preferences(BaseModel):
    startup_friendly: Optional[bool] = None
    sustainable_materials: Optional[bool] = None


class Requirement(BaseModel):
    objective: str
    entity_type: str
    hard_constraints: HardConstraints
    preferences: Preferences
    requested_results: int = 3