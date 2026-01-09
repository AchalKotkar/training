from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException

from typing import List

go=FastAPI()

class Trail(BaseModel):
    name: str
    location: str
    difficulty: str
    distance_km: float

class TrailResponse(BaseModel):
    id: int
    name: str
    
trails = [
    {"id": 1, "name": "Himalayan Base Camp", "location": "Himachal Pradesh", "difficulty": "hard", "distance_km": 12},
    {"id": 2, "name": "Valley of Flowers", "location": "Uttarakhand", "difficulty": "medium", "distance_km": 8},
    {"id": 3, "name": "Triund Trek", "location": "Himachal Pradesh", "difficulty": "easy", "distance_km": 9}
]

@go.get("/trails",  response_model=List[TrailResponse])
def get_trails(name:str=None, location:str=None, difficulty:str=None, distance_km:int=None):
    result=trails
    if name is not None:
        result=[u for u in result if u["name"]==name]
    if location is not None:
        result=[u for u in result if u["location"]==location]
    if difficulty is not None:
        result=[u for u in result if u["difficulty"]==difficulty]
    if distance_km is not None:
        result=[u for u in result if u["distance_km"]<=distance_km]
    return result

@go.get("/trails/{t_id}")
def get_trails(t_id:int):
    for t in trails:
        if t["id"]==t_id:
            return t
    #return "Trail not found with this Id"
    raise HTTPException(status_code=404, detail="Trail not found")


@go.post("/trails", status_code=201)
def create_trail(trail: Trail):
    if trail.distance_km <= 0:
        raise HTTPException(status_code=400, detail="Distance must be greater than 0")
    
    new_id = trails[-1]["id"] + 1 if trails else 1

    new_trail = {
        "id": new_id,
        "name": trail.name,
        "location": trail.location,
        "difficulty": trail.difficulty,
        "distance_km": trail.distance_km
    }

    trails.append(new_trail)
    return {
        "message": "Trail created successfully",
        "trail": new_trail
    }

@go.put("/trails/{trail_id}")
def update_trail(trail_id: int, updated_trail: Trail):
    for trail in trails:
        if trail["id"] == trail_id:
            trail["name"] = updated_trail.name
            trail["location"] = updated_trail.location
            trail["difficulty"] = updated_trail.difficulty
            trail["distance_km"] = updated_trail.distance_km

            return {
                "message": "Trail updated successfully",
                "trail": trail
            }

    #return {"error": "Trail not found"}
    raise HTTPException(status_code=404, detail="Trail not found")

@go.delete("/trails/{trail_id}")
def delete_trail(trail_id: int):
    for trail in trails:
        if trail["id"] == trail_id:
            trails.remove(trail)
            return {"message": f"Trail {trail_id} deleted successfully"}

    return {"error": "Trail not found"}


