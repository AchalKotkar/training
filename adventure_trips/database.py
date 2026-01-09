from sqlmodel import SQLModel, create_engine, Session

# SQLite file
DATABASE_URL = "sqlite:///trips.db"

# Create engine
engine = create_engine(DATABASE_URL, echo=True)  # echo=True prints SQL queries

# Function to create tables
def create_db_and_tables():
    from models import AdventureTrip
    SQLModel.metadata.create_all(engine)

# Dependency to provide a session
def get_session():
    with Session(engine) as session:
        yield session
