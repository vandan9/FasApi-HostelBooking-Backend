from uu import encode
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2, OAuth2PasswordBearer
from jose import JWTError,jwt
from datetime import datetime, timedelta, timezone

from .database import get_db
from .config import settings
from . import models
from sqlalchemy.orm import Session

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
OAuth2_schema=OAuth2PasswordBearer(tokenUrl='login')
def generate_token(data:dict):
    to_encode=data.copy()
    expire =datetime.now(timezone.utc)+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token

def verify_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:int=payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data=id
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token:str=Depends(OAuth2_schema),db:Session=Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    token=verify_token(token,credentials_exception)
    user=db.query(models.Users).filter(models.Users.user_id==token).first()
    return user