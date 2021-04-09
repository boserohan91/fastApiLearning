from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.orm import Session

from .login import get_current_user

from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(
    prefix='/blog',
    tags = ['Blog']
)

##################################################################
# PATH '/blog/{blog_id}'
##################################################################

@router.get('/{blog_id}', status_code=status.HTTP_200_OK, response_model=schemas.Blog)
def get_blog(blog_id: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    # retrieve blog with id = blog_id from db
    blog = crud.get_blog_by_id(ses=db,id=blog_id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with {blog_id} does not exist")
    return blog

@router.delete('/{blog_id}', status_code=status.HTTP_202_ACCEPTED)
def delete_blog(blog_id: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    # delete blog with id = blog_id from db
    return crud.delete_blog_by_id(ses=db,id=blog_id)

##################################################################
# PATH '/blog/author/{author}'
##################################################################

@router.get('/author/{author}', status_code=status.HTTP_200_OK, response_model=List[schemas.BlogShow])
def get_blog_by_author(author: str, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    # retrieve blog with id = blog_id from db
    blogs = crud.get_blog_by_author(ses=db,author=author)
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No blogs found for author {author}")
    return blogs

##################################################################
# PATH '/blog'
##################################################################

@router.get('', status_code=status.HTTP_200_OK)
def get_all_blogs(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return crud.get_all_blogs(ses=db)

@router.post('', status_code=status.HTTP_201_CREATED)
def post_blog(blog: schemas.BlogCreate, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    # save blog in db
    return crud.create_blog(ses=db, blog=blog)