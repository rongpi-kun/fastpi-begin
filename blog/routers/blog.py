from fastapi import HTTPException, Depends, status, APIRouter
from typing import List
from .. database import get_db
from .. import schemas
from .. import models
from .. token import get_current_user
from typing import Annotated


router = APIRouter(
    prefix='/blog',
    tags=['blogs']
)



@router.post('/', status_code=201)
def create_blog(request: schemas.Blog, db = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    print('user:', current_user.email)
    user = db.query(models.UserModel).filter(models.UserModel.email == current_user.email).first()
    new_blog = models.BlogModel(title=request.title, author=request.author, user_id = user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def all(db = Depends(get_db)):
    all_blogs = db.query(models.BlogModel).all()
    return all_blogs

@router.get('/{id}/', status_code=200, response_model=schemas.ShowBlog)
def get_blog(id, db = Depends(get_db)):
    blog = db.query(models.BlogModel).filter(models.BlogModel.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'data with {id} is not found')
    return blog

@router.put('/update/{id}/', status_code=status.HTTP_202_ACCEPTED)
def update(request: schemas.Blog, id, db = Depends(get_db)):
    blog = db.query(models.BlogModel).filter(models.BlogModel.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id: {id} does not exists')
    blog.update(request.dict())
    db.commit()
    return 'successfully updated'

@router.delete('/{id}/')
def delete(id, db = Depends(get_db)):
    blog = db.query(models.BlogModel).filter(models.BlogModel.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id: {id} does not exists')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'ok deleted'