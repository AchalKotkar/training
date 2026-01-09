from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from models import AdventureTrip
from database import engine, create_db_and_tables, get_session

app = FastAPI()

# Create tables
create_db_and_tables()

@app.get("/trips", response_model=List[AdventureTrip])
def get_trips(session: Session = Depends(get_session)):
    trips = session.exec(select(AdventureTrip)).all()
    return trips

@app.post("/trips", response_model=AdventureTrip)
def create_trip(trip: AdventureTrip, session: Session = Depends(get_session)):
    session.add(trip)
    session.commit()
    session.refresh(trip)
    return trip

@app.get("/trips/{trip_id}", response_model=AdventureTrip)
def get_trip(trip_id: int, session: Session = Depends(get_session)):
    trip = session.get(AdventureTrip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


from sqlmodel import SQLModel
from typing import Optional

class AdventureTripUpdate(SQLModel):
    name: Optional[str] = None
    destination: Optional[str] = None
    duration_days: Optional[int] = None
    cost: Optional[float] = None
    max_people: Optional[int] = None

@app.patch("/trips/{trip_id}", response_model=AdventureTrip)
def update_trip(trip_id: int, trip_update: AdventureTripUpdate, session: Session = Depends(get_session)):
    trip = session.get(AdventureTrip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    update_data = trip_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(trip, key, value)

    session.add(trip)
    session.commit()
    session.refresh(trip)
    return trip


@app.delete("/trips/{trip_id}")
def delete_trip(trip_id: int, session: Session = Depends(get_session)):
    trip = session.get(AdventureTrip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    session.delete(trip)
    session.commit()
    return {"message": "Trip deleted successfully"}
