from pydantic import BaseModel


class SearchSummary(BaseModel):
    total_suppliers: int
    product_matches: int
    capacity_matches: int
    delivery_matches: int
    final_matches: int