from .utils import get_password_hash,verify_password
from databases.config import get_db
from . import schemas,models
from sqlalchemy.orm import Session
from fastapi import Depends
from .users.db_operations import get_user




# authnticate user
def authenticate_user(username: str, password: str, db: Session):
    user = get_user(db,username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

















