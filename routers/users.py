from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from models import User
from database import SessionLocal
from .auth import get_current_user
from passlib.context import CryptContext

router =APIRouter(
    prefix="/users",
    tags=["users"]
)

# Dependency for DB session:
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



class UserVerification(BaseModel):
    password : str
    new_password : str


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency, user : user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return db.query(User).filter(User.id == user.get('id')).first()

@router.put('/change-password')
async def change_password(db: db_dependency, user: user_dependency, user_verification : UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    user_model = db.query(User).filter(User.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect old password")
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
    db.refresh(user_model)

    return {"message": "Password updated successfully"}