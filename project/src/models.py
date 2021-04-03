from .database import Base
from sqlalchemy import Column, Integer, String

class Blogs(Base):
    __tablename__ = 'blogs'

    id =  Column(Integer, primary_key=True, index=True)
    author = Column(String)
    title = Column(String)
    body = Column(String)

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)