from fastapi import FastAPI, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from project.src import models, crud, schemas
from project.src.database import SessionLocal, engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def root():
    return {"data" : {"description" : "This is the root page"}}

@app.get('/blog/{blog_id}')
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    # retrieve blog with id = blog_id from db
    return crud.get_blog_by_id(ses=db,id=blog_id)

@app.get('/blog/author/{author}')
def get_blog_comments(author: str, db: Session = Depends(get_db)):
    # retrieve blog with id = blog_id from db
    return crud.get_blog_by_author(ses=db,author=author)

@app.get('/blogs')
def get_all_blogs(db: Session = Depends(get_db)):
    return crud.get_all_blogs(ses=db)

@app.post('/blog/')
def post_blog(blog: schemas.BlogCreate, db: Session = Depends(get_db)):
    # save blog in db
    return crud.create_blog(ses=db, blog=blog)