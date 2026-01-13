from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECERET_KEY = "jwtseceret"
ALGORITHM = "HS256"
ACESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECERET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_excpetion):
    try:
        payload = jwt.decode(token, SECERET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")  # type:ignore
        if id is None:
            raise credentials_excpetion
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_excpetion
    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_excpetion = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not logged in to perform this action",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, credentials_excpetion)
    user = db.query(models.user).filter(models.User.id == token.id).first()

    return user
