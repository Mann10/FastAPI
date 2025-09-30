from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from app.models import Users
from app.database import SessionLocal
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    tags=['user']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


@router.get('/users', status_code=status.HTTP_200_OK)
async def get_user(user:dict=Depends(get_current_user) , db:Session=Depends(get_db) ):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put("/change_password", status_code=status.HTTP_200_OK)
async def change_password(user_verification: UserVerification,user:dict=Depends(get_current_user) , db:Session = Depends(get_db)):
    
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_passwprd):
        raise HTTPException(status_code=401, detail='Error on password change')
    user_model.hashed_passwprd = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()


@router.put("/change_number", status_code=status.HTTP_204_NO_CONTENT)
async def change_phonenumber(new_number: str,user:dict=Depends(get_current_user) , db:Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = new_number
    db.add(user_model)
    db.commit()
