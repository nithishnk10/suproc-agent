from typing import List, Optional
from pydantic import BaseModel, Field


class HardConstraints(BaseModel):
    # Common
    locations: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)

    # Supplier
    product_category: Optional[str] = None
    minimum_capacity: Optional[int] = None
    maximum_delivery_days: Optional[int] = None

    # Professional
    role: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    minimum_experience: Optional[int] = None

    # Opportunity
    industry: Optional[str] = None
    minimum_budget: Optional[int] = None
    priority: Optional[str] = None


class Preferences(BaseModel):
    startup_friendly: Optional[bool] = None
    sustainable_materials: Optional[bool] = None


class Requirement(BaseModel):
    objective: str
    entity_type: str
    hard_constraints: HardConstraints
    preferences: Preferences
    requested_results: int = 3