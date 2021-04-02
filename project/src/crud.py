from sqlalchemy.orm import Session
from . import models, schemas


def get_all_blogs(ses: Session):
    return ses.query(models.Blogs).all()

def get_blog_by_id(ses: Session, id: int):
    return ses.query(models.Blogs).filter(models.Blogs.id == id).first()

def get_blog_by_author(ses: Session, author: str):
    return ses.query(models.Blogs).filter(models.Blogs.author_name == author).all()

def create_blog(ses: Session, blog: schemas.BlogCreate):
    new_blog = models.Blogs(author_name=blog.author, blog_title=blog.title, blog_body=blog.body)
    ses.add(new_blog)
    ses.commit()
    ses.refresh(new_blog)
    return {f"{new_blog.blog_title} added with id: {new_blog.id} in blogs"}