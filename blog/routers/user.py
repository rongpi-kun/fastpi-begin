from fastapi import HTTPException, Depends, status, APIRouter
from typing import List
from .. database import get_db
from .. import schemas
from .. import models
from passlib.context import CryptContext

router = APIRouter()

passwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

@router.post('/register/', response_model=schemas.ShowUser, tags=['users'])
def create_user(request: schemas.User, db = Depends(get_db)):
    hashPassword = passwd_context.hash(request.password)
    new_user = models.UserModel(name=request.name, email=request.email, password=hashPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/user/{id}/', response_model=schemas.ShowUser, tags=['users'])
def get_user(id: int, db = Depends(get_db)):
    user = db.query(models.UserModel).filter(models.UserModel.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} is not found')
    return user

@router.get('/user/', response_model=List[schemas.ShowUser], tags=['users'], status_code=status.HTTP_200_OK)
def all_user(db = Depends(get_db)):
    users = db.query(models.UserModel).all()
    return users