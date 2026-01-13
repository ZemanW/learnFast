from fastapi import FastAPI, Depends, APIRouter, Response,HTTPException,status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models,schemas,utils,oauth2
from ..database import get_db
router = APIRouter(
    prefix="/login"
)

@router.post("/")
def login(user_credentials : OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()#type:ignore
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    if not utils.verify_pwd(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentails")
    
    acess_token = oauth2.create_access_token(data={
        "user_id":user.id,
    })
    
    return {"access_token":acess_token,"token_type":"bearer"}



