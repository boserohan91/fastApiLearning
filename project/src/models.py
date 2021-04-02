from .database import Base
from sqlalchemy import Column, Integer, String

class Blogs(Base):
    __tablename__ = 'blogs'

    id =  Column(Integer, primary_key=True, index=True)
    author_name = Column(String)
    blog_title = Column(String)
    blog_body = Column(String)