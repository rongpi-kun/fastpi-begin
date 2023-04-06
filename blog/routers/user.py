from fastapi import HTTPException, Depends, status, APIRouter
from typing import List
from .. database import get_db
from .. import schemas
from .. import models
from passlib.context import CryptContext
from .. import token

router = APIRouter(
    tags=['users']
)

passwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

@router.post('/register/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db = Depends(get_db)):
    hashPassword = passwd_context.hash(request.password)
    new_user = models.UserModel(name=request.name, email=request.email, password=hashPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/user/{id}/', response_model=schemas.ShowUser)
def get_user(id: int, db = Depends(get_db), current_user: schemas.User = Depends(token.get_current_user)):
    user = db.query(models.UserModel).filter(models.UserModel.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} is not found')
    return user

@router.get('/user/', response_model=List[schemas.ShowUser], status_code=status.HTTP_200_OK)
def all_user(db = Depends(get_db), current_user: schemas.User = Depends(token.get_current_user)):
    users = db.query(models.UserModel).all()
    return users