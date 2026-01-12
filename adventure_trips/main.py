from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from models import AdventureTrip, AdventureTripRead, AdventureTripUpdate
from database import create_db_and_tables, get_session

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()


@app.get("/trips", response_model=List[AdventureTripRead])
async def get_trips(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(AdventureTrip))
    trips = result.scalars().all()
    return trips


@app.post("/trips", response_model=AdventureTripRead)
async def create_trip(
    trip: AdventureTrip,
    session: AsyncSession = Depends(get_session)
):
    session.add(trip)
    await session.commit()
    await session.refresh(trip)
    return trip

@app.get("/trips/{trip_id}", response_model=AdventureTripRead)
async def get_trip(
    trip_id: int,
    session: AsyncSession = Depends(get_session)
):
    trip = await session.get(AdventureTrip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

@app.patch("/trips/{trip_id}", response_model=AdventureTrip)
async def update_trip(
    trip_id: int,
    trip_update: AdventureTripUpdate,
    session: AsyncSession = Depends(get_session)
):
    trip = await session.get(AdventureTrip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    for key, value in trip_update.dict(exclude_unset=True).items():
        setattr(trip, key, value)

    session.add(trip)
    await session.commit()
    await session.refresh(trip)
    return trip

@app.delete("/trips/{trip_id}")
async def delete_trip(
    trip_id: int,
    session: AsyncSession = Depends(get_session)
):
    trip = await session.get(AdventureTrip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    await session.delete(trip)
    await session.commit()
    return {"message": "Trip deleted successfully"}
