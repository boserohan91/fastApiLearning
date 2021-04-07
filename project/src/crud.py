from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import Response, status, HTTPException


def get_all_blogs(ses: Session):
    return ses.query(models.Blogs).all()

def get_blog_by_id(ses: Session, id: int):
    return ses.query(models.Blogs).filter(models.Blogs.id == id).first()

def delete_blog_by_id(ses: Session, id: int):
    del_code = ses.query(models.Blogs).filter(models.Blogs.id == id).delete()
    if del_code == 1:
        ses.commit()
        return {"Deletion Successful!"}
    elif del_code == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not available")
    else:
        raise HTTPException(status_code=status.HTTP_300_MULTIPLE_CHOICES,
                            detail="There are more than one document with the same id to be deleted. Deletion Error!")
    return

def get_blog_by_author(ses: Session, author: str):
    return ses.query(models.Blogs).filter(models.Blogs.user.has(models.Users.name==author)).all()

def create_blog(ses: Session, blog: schemas.BlogCreate):
    new_blog = models.Blogs(user_id=blog.user_id, title=blog.title, body=blog.body)
    ses.add(new_blog)
    ses.commit()
    ses.refresh(new_blog)
    return {f"{new_blog.title} added with id: {new_blog.id} in blogs"}

def create_user(ses: Session, user: schemas.User):
    new_user = models.Users(**user.dict())
    ses.add(new_user)
    ses.commit()
    ses.refresh(new_user)
    return {f"{new_user.email} added to Users"}

def get_user(ses: Session, email: str):
    user = ses.query(models.Users).filter(models.Users.email == email).one()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid User/User does not exist")
    else:
        return user