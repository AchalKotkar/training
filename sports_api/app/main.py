from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routes import matches

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(matches.router)
