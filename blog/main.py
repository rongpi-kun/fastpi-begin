from fastapi import FastAPI, Depends, status, HTTPException
from . import schemas
import uvicorn
from . import models
from .database import engine, SessionLocal
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog/', status_code=201, tags=['blogs'])
def create_blog(request: schemas.Blog, db = Depends(get_db)):
    new_blog = models.BlogModel(title=request.title, author=request.author)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog/', status_code=status.HTTP_200_OK, tags=['blogs'])
def all(db = Depends(get_db)):
    all_blogs = db.query(models.BlogModel).all()
    return all_blogs

@app.get('/blog/{id}/', status_code=200, tags=['blogs'])
def get_blog(id, db = Depends(get_db)):
    blog = db.query(models.BlogModel).filter(models.BlogModel.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'data with {id} is not found')
    return blog

@app.put('/blog/update/{id}/', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(request: schemas.Blog, id, db = Depends(get_db)):
    blog = db.query(models.BlogModel).filter(models.BlogModel.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id: {id} does not exists')
    blog.update(request.dict())
    db.commit()
    return 'successfully updated'

@app.delete('/blog/{id}/', tags=['blogs'])
def delete(id, db = Depends(get_db)):
    blog = db.query(models.BlogModel).filter(models.BlogModel.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id: {id} does not exists')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'ok deleted'


passwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

@app.post('/register/', response_model=schemas.ShowUser, tags=['users'])
def create_user(request: schemas.User, db = Depends(get_db)):
    hashPassword = passwd_context.hash(request.password)
    new_user = models.UserModel(name=request.name, email=request.email, password=hashPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}/', response_model=schemas.ShowUser, tags=['users'])
def get_user(id: int, db = Depends(get_db)):
    user = db.query(models.UserModel).filter(models.UserModel.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} is not found')
    return user

@app.get('/user/', response_model=List[schemas.ShowUser], tags=['users'], status_code=status.HTTP_200_OK)
def all_user(db = Depends(get_db)):
    users = db.query(models.UserModel).all()
    return users

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)