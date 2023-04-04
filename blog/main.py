from fastapi import FastAPI
from . import schemas
import uvicorn

app = FastAPI()

@app.post('/blog/')
def create_blog(blog: schemas.Blog):
    return blog

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)