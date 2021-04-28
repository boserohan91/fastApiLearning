from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from .. import crud, models, schemas
from ..database import get_db


router = APIRouter(
    prefix='/user',
    tags=['User']
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

##################################################################
# PATH '/user'
##################################################################
@router.post('', status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.User, db: Session = Depends(get_db)):
    # get hashed password
    hashed_pwd = pwd_context.hash(user.password)
    user.password = hashed_pwd
    # save user in db
    return (await crud.create_user(ses=db, user=user))

@router.get('', status_code=status.HTTP_200_OK, response_model= schemas.UserBase)
async def get_user(email: str, db: Session = Depends(get_db)):
    return (await crud.get_user(email=email, ses=db))