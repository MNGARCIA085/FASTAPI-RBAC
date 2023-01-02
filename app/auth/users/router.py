from fastapi import Depends, APIRouter
from .. import schemas,dependencies
from . import db_operations
from sqlalchemy.orm import Session
from databases.config import get_db



router = APIRouter(
    prefix="/users",
    responses={404: {"description": "Not found"}},
)



# get all users
@router.get("/",response_model=list[schemas.UserOut])
def read_groups(
            skip: int = 0, 
            limit: int = 100, 
            db: Session = Depends(get_db),
        ):
        return db_operations.get_users(skip,limit,db)



# Create an user and its groups
@router.post("/")
def create_user(user:schemas.UserRegister,groups:list[int],db: Session = Depends(get_db)):
    return db_operations.create_user_groups(user,groups,db)


# Edit an user
@router.put("/{user_id}")
def edit_user(user_id:int,groups:list[int],user:schemas.User,db: Session = Depends(get_db)):
    return db_operations.edit_user(user_id,groups,user,db)


# ejemplos de uso de las dependencias
@router.get("/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(dependencies.get_current_active_user)):
    return current_user



