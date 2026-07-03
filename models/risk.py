from typing import List
from pydantic import BaseModel


class SupplierRisk(BaseModel):
    supplier_id: str
    supplier_name: str
    risks: List[str]