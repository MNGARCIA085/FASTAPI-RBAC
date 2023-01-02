from datetime import timedelta
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from . import schemas,dependencies,utils,db_operations
from sqlalchemy.orm import Session
from databases.config import get_db
from constants import ACCESS_TOKEN_EXPIRE_MINUTES
from .groups import router as groups_routes


router = APIRouter(
    prefix="/auth",
    responses={404: {"description": "Not found"}},
    tags=['auth']
)


router.include_router(groups_routes.router,tags=['groups'])


# sign up o register
@router.post("/signup", response_model=schemas.Token, summary="Sign up (register)")
async def signin(user:schemas.UserRegister,
                groups:list[int],
                db:Session = Depends(get_db)):
    # chequeo que no se haya registrado ya
    aux = db_operations.get_user(db,user.username) # devuelve False si no está
    if aux:
        raise HTTPException(status_code=400,detail='User already register') 
    # que los passwords ingresados coincidan
    if user.password != user.password_two:
        raise HTTPException(status_code=400,detail='Passwords did not match')
    # sino procedo a crear el usuario
    user = db_operations.create_user(user,groups,db)
    # creo el token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# obtener un token
@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    user = db_operations.authenticate_user(form_data.username, form_data.password,db )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}






# get all users
@router.get("/users",response_model=list[schemas.UserOut])
def read_groups(
            skip: int = 0, 
            limit: int = 100, 
            db: Session = Depends(get_db),
        ):
        return db_operations.get_users(skip,limit,db)





# Edit an user
@router.put("/users/{user_id}")
def edit_user(user_id:int,groups:list[int],user:schemas.User,db: Session = Depends(get_db)):
    return db_operations.edit_user(user_id,groups,user,db)








# ejemplos de uso de las dependencias
@router.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(dependencies.get_current_active_user)):
    return current_user



