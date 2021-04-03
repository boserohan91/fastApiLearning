from pydantic import BaseModel

class BlogBase(BaseModel):
    title: str
    author: str
    body: str

    class Config:
        orm_mode = True

class BlogCreate(BlogBase):
    pass

class Blog(BlogCreate):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True

class User(UserBase):
    password: str

class UserDB(User):
    id: int