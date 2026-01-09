from fastapi import FastAPI

app = FastAPI()


fake_users_db = {
     "achal": {
         "username": "achal",
         "full_name": "Achal Kotkar",
         "email": "achalk@example.com",
         "hashed_password": "$2b$12$7.dMpOK74IVZ1MoGMmEWceOcqtdLN/sB.vqCnVTuy.MZ1YeXnHi2e",  # bcrypt hash
         "disabled": False,
     }
 }


#----Password Hashing Utilities----
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# password = "test"
# password = password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
# print(len(password.encode("utf-8")))
# print(pwd_context.hash(password))

def verify_password(plain_password, hashed_password):
     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)


#----OAuth2 Password Flow----
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


#----JWT Configuration----
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


#----Create JWT Token----
# (Produces signed JWT string)
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt


#----User Authentication Logic----
def get_user(db, username: str):
    return db.get(username)  # Fetch user from DB

def authenticate_user(username: str, password: str):
    user = get_user(fake_users_db, username)
    if not user:
        return False

    if not verify_password(password, user["hashed_password"]):
        return False

    return user

#Returns user object, not token


#----Login Endpoint (/token)----
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(
        form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(
        data={"sub": user["username"]}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


#----Decode & Verify JWT----
from jose import JWTError

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(fake_users_db, username)
    if user is None:
        raise credentials_exception
    return user


#----Protected Route----
@app.get("/users/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
