from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class BlogBase(BaseModel):
    title: str
    body: str

    class Config:
        orm_mode = True
    
class BlogShow(BlogBase):
    user: UserBase

    class Config:
        orm_mode = True

class BlogCreate(BlogBase):
    user_id: int
    pass

class Blog(BlogShow):
    id: int

    class Config:
        orm_mode = True

class User(UserBase):
    password: str

class UserDB(User):
    id: int

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str