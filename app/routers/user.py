from fastapi import  status , HTTPException , Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas,utils
from ..database import get_db

router = APIRouter(
    prefix="/user",
    tags=["User"]
)
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    hashed_pwd = utils.hash_pwd(user.password)
    user.password = hashed_pwd
    if user:
        user_dict = user.dict()
        new_user = models.User(**user_dict)
        db.add(new_user)
        db.commit()
        return new_user
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.UserOut)
def get_one_user(id:int,db:Session=Depends(get_db)):
    one_user= db.query(models.User).filter(models.User.id == id).first()#type:ignore
    if one_user is None:
                raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return one_user




