from datetime import datetime, timedelta
import os

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from typing_extensions import Annotated
from typing import Union

from schemas import User, Token, TokenData, UserInDB
from database.models import User
from database.connection import get_db


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


auth_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(username: str):
    iterator = get_db() 
    session = next(iterator)
    try:
        user = session.query(User).filter(User.username == username).one()
        return UserInDB(username=user.username, hashed_password=user.password, active=user.active)
    except NoResultFound:
        return False
        

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def validate_token(token: Annotated[str, Depends(auth_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception(f"Invalid token {e}")
        token_data = TokenData(username=username)
    except JWTError as e:
        print(e)
        raise credentials_exception(f"Invalid token: {e}")
    user = get_user(username=token_data.username)
    if user:
        if user.active:
            return user
        else:
            raise credentials_exception("User is not active or token has expired")
            
    else:
        raise credentials_exception("Username does not exist")


async def get_current_active_user(
    current_user: Annotated[User, Depends(validate_token)]
):
    if not current_user.disabled:
        return current_user


def credentials_exception(detail):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials: {detail}",
        headers={"WWW-Authenticate": "Bearer"},
    )