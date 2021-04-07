from fastapi import FastAPI, HTTPException, Depends, status, Response 
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from project.src import models, crud, schemas
from project.src.database import SessionLocal, engine
from sqlalchemy.orm import Session

from project.src.routers import blog, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(blog.router)
app.include_router(user.router)

##################################################################
# PATH '/'
##################################################################

@app.get('/', status_code=status.HTTP_200_OK)
def root():
    return {"data" : {"description" : "This is the root page"}}