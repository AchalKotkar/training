from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.schemas import MatchUpdate
from typing import List
from typing import Optional

from app.database import get_session
from app.models import Match
from app.schemas import MatchCreate, MatchResponse

router = APIRouter(prefix="/matches", tags=["Matches"])


@router.post("/", response_model=MatchResponse)
def create_match(
    match: MatchCreate,
    session: Session = Depends(get_session)
):
    new_match = Match(
        **match.dict()
    )
    session.add(new_match)
    session.commit()
    session.refresh(new_match)
    return new_match


@router.get("/", response_model=list[MatchResponse])
def get_all_matches(
    session: Session = Depends(get_session)
):
    matches = session.exec(select(Match)).all()
    return matches


@router.get("/{match_id}", response_model=MatchResponse)
def get_match_by_id(
    match_id: int,
    session: Session = Depends(get_session)
):
    match = session.get(Match, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match

@router.patch("/{match_id}", response_model=MatchResponse)
def update_match(
    match_id: int,
    match_update: MatchUpdate,
    session: Session = Depends(get_session)
):
    match = session.get(Match, match_id)

    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    update_data = match_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(match, key, value)

    session.add(match)
    session.commit()
    session.refresh(match)

    return match


@router.get("/", response_model=list[MatchResponse])
def get_matches(
    status: Optional[str] = None,
    venue: Optional[str] = None,
    team: Optional[str] = None,
    session: Session = Depends(get_session)
):
    query = select(Match)

    if status:
        query = query.where(func.lower(Match.status) == status.lower())
    if venue:
        query = query.where(Match.venue == venue)

    if team:
        query = query.where(
            (Match.team_a == team) | (Match.team_b == team)
        )

    matches = session.exec(query).all()
    return matches

