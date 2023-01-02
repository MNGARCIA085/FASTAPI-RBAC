from typing import List, Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str | None = None
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

    class Config:
        orm_mode = True






class UserInDB(User):
    #id:int
    hashed_password: str


class UserRegister(User):
    password: str
    password_two: str


class Group(BaseModel):
    description: str | None = None

    class Config:
        orm_mode = True




# response models
class UserOut(User):
    id:int
    groups: Optional[List[Group]]

    class Config:
        orm_mode = True




class GroupOut(Group):
    id:int
    users: Optional[List[User]]

    class Config:
        orm_mode = True


    






