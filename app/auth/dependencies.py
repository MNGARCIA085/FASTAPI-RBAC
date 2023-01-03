from fastapi import Depends, HTTPException, status
from typing import List
from jose import JWTError, jwt
from . import schemas,models
from .users import db_operations
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from databases.config import get_db
from config import settings
from constants import ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login") # /token
#http://127.0.0.1:8000/auth/token


async def get_current_user(token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db_operations.get_user(db, username=token_data.username)  
    if user is None:
        raise credentials_exception
    return user.__dict__ # convierto a dict; antes user
    


async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if current_user['disabled']: # .disabled
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



# dependencia respecto a los grupos
class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles
 
    def __call__(self,user: schemas.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
        grupos = db.query(models.UserGroups).filter(models.UserGroups.user_id==user['id'])
        for g in grupos:
            print(g.group_id)
            print(self.allowed_roles)
            if g.group_id in self.allowed_roles:
                return
        #logger.debug(f"User with role {user.role} not in {self.allowed_roles}")
        raise HTTPException(status_code=403, detail="Operation not permitted")
