from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.orm import Session

from .login import get_current_user

from .. import crud, models, schemas
from ..database import get_db

import requests
from requests import HTTPError

router = APIRouter(
    prefix='/blog',
    tags = ['Blog']
)

google_key = "AIzaSyCZ5fXW3bKiQCLwG7hLa84tpS1ZIm4PM0k"

##################################################################
# PATH '/blog/{blog_id}'
##################################################################

@router.get('/{blog_id}', status_code=status.HTTP_200_OK, response_model=schemas.Blog)
async def get_blog(blog_id: int, translate_to: str = None, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    # retrieve blog with id = blog_id from db
    blog = await crud.get_blog_by_id(ses=db,id=blog_id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with {blog_id} does not exist")
    if translate_to is not None:
        translate_url = "https://translation.googleapis.com/language/translate/v2"
        payload = {
            'q' : blog.body,
            'target' : translate_to,
            'key' : google_key
        }
        try:
            response = requests.post(translate_url,params=payload)
            response.raise_for_status()
            blog.body = response.text
        except HTTPError as err:
            blog.body = f'Error: {err}'
        
    return blog


@router.delete('/{blog_id}', status_code=status.HTTP_202_ACCEPTED)
async def delete_blog(blog_id: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    # delete blog with id = blog_id from db
    return (await crud.delete_blog_by_id(ses=db,id=blog_id))

##################################################################
# PATH '/blog/author/{author}'
##################################################################

@router.get('/author/{author}', status_code=status.HTTP_200_OK, response_model=List[schemas.BlogShow])
async def get_blog_by_author(author: str, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    # retrieve blog with id = blog_id from db
    blogs = await crud.get_blog_by_author(ses=db,author=author)
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No blogs found for author {author}")
    return blogs

##################################################################
# PATH '/blog'
##################################################################

@router.get('', status_code=status.HTTP_200_OK)
async def get_all_blogs(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return (await crud.get_all_blogs(ses=db))

@router.post('', status_code=status.HTTP_201_CREATED)
async def post_blog(blog: schemas.BlogCreate, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    # save blog in db
    return (await crud.create_blog(ses=db, blog=blog))