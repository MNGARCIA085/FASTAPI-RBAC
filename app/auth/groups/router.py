from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from ..dependencies import RoleChecker
from databases.config import get_db
from .. import schemas
from . import db_operations


# por id es mejor; 1:admin
allow_create_resource = RoleChecker([1])


router = APIRouter(
    prefix="/groups",
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(allow_create_resource)],
)


# create a new group
@router.post("/",status_code=201)
def create_group(group: schemas.Group, db: Session = Depends(get_db)):
    return db_operations.post_group(group,db)


# list of all groups
@router.get("/",response_model=list[schemas.GroupOut])
def read_groups(
            skip: int = 0, 
            limit: int = 100, 
            db: Session = Depends(get_db),
        ):
        return db_operations.get_groups(skip,limit,db)



# get group by id
@router.get("/{group_id}",response_model=schemas.GroupOut)
def read_user(group_id,db: Session = Depends(get_db)):
    return db_operations.get_group_by_id(group_id,db)




# Delete a group
@router.delete("/{group_id}")
def delete_user(group_id,db: Session = Depends(get_db)):
    return db_operations.delete_group(group_id,db)