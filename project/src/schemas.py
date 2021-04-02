from pydantic import BaseModel

class BlogBase(BaseModel):
    title: str
    author: str
    body: str

class BlogCreate(BlogBase):
    pass

class Blog(BlogCreate):
    id: int