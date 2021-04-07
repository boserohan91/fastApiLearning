from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, crud
from .user import pwd_context


router = APIRouter(
    prefix='/login',
    tags=['Authentication']
)

@router.post('', status_code=status.HTTP_202_ACCEPTED)
def auth_to_get_token(auth: schemas.Login, db: Session = Depends(database.get_db)):
    hashed_password = (crud.get_user(db, auth.username)).password
    if not pwd_context.verify(auth.password, hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Incorrect Credentials")
    # create and return JWT token
    return {"Authenticated"}