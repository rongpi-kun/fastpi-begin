from fastapi import HTTPException, Depends, status, APIRouter
from typing import List
from .. database import get_db
from .. import schemas
from .. import models

router = APIRouter()

@router.post('/blog/', status_code=201, tags=['blogs'])
def create_blog(request: schemas.Blog, db = Depends(get_db)):
    new_blog = models.BlogModel(title=request.title, author=request.author, user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get('/blog/', status_code=status.HTTP_200_OK, tags=['blogs'], response_model=List[schemas.ShowBlog])
def all(db = Depends(get_db)):
    all_blogs = db.query(models.BlogModel).all()
    return all_blogs

@router.get('/blog/{id}/', status_code=200, tags=['blogs'], response_model=schemas.ShowBlog)
def get_blog(id, db = Depends(get_db)):
    blog = db.query(models.BlogModel).filter(models.BlogModel.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'data with {id} is not found')
    return blog

@router.put('/blog/update/{id}/', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(request: schemas.Blog, id, db = Depends(get_db)):
    blog = db.query(models.BlogModel).filter(models.BlogModel.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id: {id} does not exists')
    blog.update(request.dict())
    db.commit()
    return 'successfully updated'

@router.delete('/blog/{id}/', tags=['blogs'])
def delete(id, db = Depends(get_db)):
    blog = db.query(models.BlogModel).filter(models.BlogModel.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id: {id} does not exists')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'ok deleted'