from ..utils import get_password_hash
from databases.config import get_db
from .. import schemas,models
from sqlalchemy.orm import Session
from fastapi import Depends



# create user
def create_user(user: schemas.UserRegister,
                groups: list[int],
                db: Session = Depends(get_db)):
    hash_password = get_password_hash(user.password)
    db_user = models.User(email=user.email,
                          full_name=user.full_name,
                          hashed_password=hash_password,
                          username=user.username)
    db.add(db_user)
    db.flush() # para poder obtener el id
    user_id = db_user.id
    for g in groups:
        #aux = verificar que el grupo exista
        #if aux
        db_item = models.UserGroups(user_id=user_id,group_id=g)
        db.add(db_item)
    db.commit()
    db.refresh(db_user)
    return db_user
    # obs. si es una lista vacía poner std por defecto.



# edit an user; his data and also his groups
def edit_user(user_id: int, groups:list[int],user: schemas.User,db: Session = Depends(get_db)):
    # std data
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(db_user, key, value)
    # lista de grupos
    db.query(models.UserGroups).filter_by(user_id=user_id).delete()
    # inserto
    for g in groups:
        db_userGroups = models.UserGroups(user_id=user_id,group_id=g)
        db.add(db_userGroups)
    db.refresh(db_user)
    db.commit()
    return {'Msg':"Operation succeed"} 



# get all users
def get_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
    ):
    return db.query(models.User).offset(skip).limit(limit).all()













