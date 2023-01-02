from datetime import timedelta
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from . import schemas,utils
from sqlalchemy.orm import Session
from databases.config import get_db
from constants import ACCESS_TOKEN_EXPIRE_MINUTES
from .groups import router as groups_routes
from .users import db_operations, router as users_routes


router = APIRouter(
    prefix="/auth",
    responses={404: {"description": "Not found"}},
)


router.include_router(groups_routes.router,tags=['groups'])
router.include_router(users_routes.router,tags=['users'])


# sign up o register
@router.post("/signup", response_model=schemas.Token, summary="Sign up (register)",tags=['auth'])
async def signin(user:schemas.UserRegister,
                db:Session = Depends(get_db)):
    # chequeo que no se haya registrado ya
    aux = db_operations.get_user(db,user.username) # devuelve False si no está
    if aux:
        raise HTTPException(status_code=400,detail='User already register') 
    # que los passwords ingresados coincidan
    if user.password != user.password_two:
        raise HTTPException(status_code=400,detail='Passwords did not match')
    # sino procedo a crear el usuario
    user = db_operations.create_user(user,db)
    # creo el token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# obtener un token
@router.post("/login", response_model=schemas.Token, tags=['auth'])
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






