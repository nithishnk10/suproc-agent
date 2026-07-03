from typing import List
from pydantic import BaseModel


class MissingInformation(BaseModel):
    items: List[str]