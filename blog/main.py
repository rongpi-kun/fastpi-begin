from fastapi import FastAPI
import uvicorn
from . import models
from .database import engine
from . routers import blog, user, login
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    'http://127.0.0.1:5500',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods = ['*'],
    allow_headers = ['*'],
)

app.include_router(login.router)
app.include_router(user.router)
app.include_router(blog.router)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)