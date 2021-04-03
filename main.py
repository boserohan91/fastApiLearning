from fastapi import FastAPI, HTTPException, Depends, status, Response 
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from project.src import models, crud, schemas
from project.src.database import SessionLocal, engine
from sqlalchemy.orm import Session
from passlib.context import CryptContext

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

##################################################################
# PATH '/'
##################################################################

@app.get('/', status_code=status.HTTP_200_OK)
def root():
    return {"data" : {"description" : "This is the root page"}}

##################################################################
# PATH '/blog/{blog_id}'
##################################################################

@app.get('/blog/{blog_id}', status_code=status.HTTP_200_OK, response_model=schemas.Blog)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    # retrieve blog with id = blog_id from db
    blog = crud.get_blog_by_id(ses=db,id=blog_id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with {blog_id} does not exist")
    return blog

@app.delete('/blog/{blog_id}', status_code=status.HTTP_202_ACCEPTED)
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    # delete blog with id = blog_id from db
    return crud.delete_blog_by_id(ses=db,id=blog_id)

##################################################################
# PATH '/blog/author/{author}'
##################################################################

@app.get('/blog/author/{author}', status_code=status.HTTP_200_OK, response_model=List[schemas.BlogBase])
def get_blog_by_author(author: str, db: Session = Depends(get_db)):
    # retrieve blog with id = blog_id from db
    blogs = crud.get_blog_by_author(ses=db,author=author)
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No blogs found for author {author}")
    return blogs

##################################################################
# PATH '/blog'
##################################################################

@app.get('/blog', status_code=status.HTTP_200_OK)
def get_all_blogs(db: Session = Depends(get_db)):
    return crud.get_all_blogs(ses=db)

@app.post('/blog', status_code=status.HTTP_201_CREATED)
def post_blog(blog: schemas.BlogCreate, db: Session = Depends(get_db)):
    # save blog in db
    return crud.create_blog(ses=db, blog=blog)


##################################################################
# PATH '/user'
##################################################################
@app.post('/user', status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    # get hashed password
    hashed_pwd = pwd_context.hash(user.password)
    user.password = hashed_pwd
    # save blog in db
    return crud.create_user(ses=db, user=user)

@app.get('/user', status_code=status.HTTP_200_OK, response_model= schemas.UserBase)
def get_user(email: str, db: Session = Depends(get_db)):
    return crud.get_user(email=email, ses=db)