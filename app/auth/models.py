from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from databases.config import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    full_name = Column(String)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)
    groups = relationship('Groups',secondary='users_groups')


class Groups(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    users = relationship('User',secondary='users_groups')


class UserGroups(Base):
    __tablename__ = 'users_groups'
    user_id = Column(Integer, ForeignKey('users.id'),primary_key=True)
    group_id = Column(Integer,ForeignKey('groups.id'),primary_key=True)




"""

	
alembic revision --autogenerate -m "Added user table"
alembic upgrade head

"""