from sqlmodel import SQLModel, Field
from typing import Optional

class Match(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    team_a: str
    team_b: str
    venue: str
    match_date: str
    team_a_score: int = 0
    team_b_score: int = 0
    status: str = "scheduled"
