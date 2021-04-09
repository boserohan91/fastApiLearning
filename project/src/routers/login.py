from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
from .. import schemas, database, crud
from .user import pwd_context

ALGORITHM = "HS256"
SECRET_KEY = "6e7c986444db4ab59bfd17d72c847fd29befced6d2dc9c834b626821526ecac7"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter(
    prefix='/login',
    tags=['Authentication']
)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credential_exception
    db = database.SessionLocal()
    user = crud.get_user(email=token_data.username, ses=db)
    db.close()
    if user is None:
        raise credential_exception
    return user
    
    

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post('', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Token)
def auth_to_get_token(auth_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    hashed_password = (crud.get_user(db, auth_data.username)).password
    if not pwd_context.verify(auth_data.password, hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Incorrect Credentials")
    # create and return JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub":auth_data.username},
                                             expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}