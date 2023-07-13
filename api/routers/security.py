from datetime import timedelta, datetime
from typing_extensions import Annotated


from fastapi import Depends, HTTPException, APIRouter, status
from schemas import Token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..security_utils import authenticate_user, create_access_token
from database.connection import get_db

ACCESS_TOKEN_EXPIRE_HOURS = 1


router = APIRouter()


@router.post("/token", response_model=Token, include_in_schema=False)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
