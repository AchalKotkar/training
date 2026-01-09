from sqlmodel import SQLModel, Field
from typing import Optional

class AdventureTrip(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    destination: str
    duration_days: int
    cost: float
    max_people: int
