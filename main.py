from fastapi import FastAPI

app = FastAPI()

@app.get('/blog/{id}')
def index(id: int):
    return {'id': id,
        'data': {'name': 'Kutta Kalia'}
        }

@app.get('/about')
def about():
    return {'msg': 'about page'}

@app.post('/blog')
def create_blog():
    return {
        'msg': 'blog created'
    }