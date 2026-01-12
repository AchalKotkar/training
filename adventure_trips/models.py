from sqlmodel import SQLModel, Field
from typing import Optional

# --------------------
# DB TABLE MODEL
# --------------------
class AdventureTrip(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    destination: str
    duration_days: int
    cost: float
    max_people: int


# --------------------
# RESPONSE SCHEMA
# --------------------
class AdventureTripRead(SQLModel):
    id: int
    name: str
    destination: str
    duration_days: int
    cost: float
    max_people: int


# --------------------
# UPDATE SCHEMA
# --------------------
class AdventureTripUpdate(SQLModel):
    name: Optional[str] = None
    destination: Optional[str] = None
    duration_days: Optional[int] = None
    cost: Optional[float] = None
    max_people: Optional[int] = None
