from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from models import User, UserCreate, UserRead
from database import get_session, create_db_and_tables
from auth import hash_password, verify_password, create_access_token, get_current_user

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()


@app.post("/register", response_model=UserRead)
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.username == user.username))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    db_user = User(
        username=user.username,
        hashed_password=hash_password(user.password)
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


@app.post("/login")
async def login(user: UserCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.username == user.username))
    db_user = result.scalars().first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/me")
async def read_me(current_user: str = Depends(get_current_user)):
    return {
        "message": "Access granted",
        "user": current_user
    }

# Hardcoded access token value just for once to see how GET request looks

# SECRET_KEY = "supersecretkey"
# ALGORITHM = "HS256"
# @app.get("/test-hardcoded-token")
# async def test_token():
#     hardcoded_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhY2hhbCIsImV4cCI6MTc2ODIyMTUwN30.jRgNYnRuyMLtIoPIb8hZmu9oHPs53YtzKE74B946b3g"

#     try:
#         payload = jwt.decode(hardcoded_token, SECRET_KEY, algorithms=[ALGORITHM])
#         username = payload.get("sub")

#         if not username:
#             raise HTTPException(status_code=401, detail="Invalid token")

#         return {
#             "message": "Access granted",
#             "username": username
#         }

#     except JWTError:
#         raise HTTPException(status_code=401, detail="Access denied")
