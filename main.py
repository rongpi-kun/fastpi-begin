from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {'data': {'name': 'Kutta Kalia'}}

@app.get('/about')
def about():
    return {'msg': 'about page'}