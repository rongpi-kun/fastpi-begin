# from fastapi import FastAPI
# from pydantic import BaseModel
# import uvicorn

# class Blog(BaseModel):
#     title : str
#     author : str

# app = FastAPI()

# @app.get('/blog/{id}')
# def index(id: int):
#     return {'id': id,
#         'data': {'name': 'Kutta Kalia'}
#         }

# @app.get('/about')
# def about():
#     return {'msg': 'about page'}

# @app.post('/blog')
# def create_blog(blog: Blog):
#     return blog

# if __name__ == '__main__':
#     uvicorn.run(app, host='127.0.0.1', port=9000)