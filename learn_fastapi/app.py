from fastapi import FastAPI
from pydantic import BaseModel

application=FastAPI()

class movie(BaseModel):
    title:str
    director:str
    year:int

movies = [
    {"id": 1, "title": "3 Idiots", "director": "Rajkumar Hirani", "year": 2009},
    {"id": 2, "title": "Dangal", "director": "Nitesh Tiwari", "year": 2016},
    {"id": 3, "title": "PK", "director": "Rajkumar Hirani", "year": 2014},
    {"id": 4, "title": "Chhichhore", "director": "Nitesh Tiwari", "year": 2019}
]

@application.get("/movies")
def get_movies(title:str=None, director:str=None, year:int=None):
    result=movies
    if title is not None:
        result=[u for u in result if u["title"]==title]
    if director is not None:
        result=[u for u in result if u["director"]==director]
    if year is not None:
        result=[u for u in result if u["year"]==year]
    return result


@application.get("/movies/{m_id}")
def get_movies(m_id:int):
    for m in movies:
        if m["id"]==m_id:
            return m
    return "Movie not found"