from sqlmodel import SQLModel
from typing import Optional
from typing import Optional
from sqlmodel import SQLModel

class MatchCreate(SQLModel):
    team_a: str
    team_b: str
    venue: str
    match_date: str

class MatchResponse(SQLModel):
    id: int
    team_a: str
    team_b: str
    venue: str
    match_date: str
    team_a_score: int
    team_b_score: int
    status: str

class MatchUpdate(SQLModel):
    team_a_score: Optional[int] = None
    team_b_score: Optional[int] = None
    status: Optional[str] = None
