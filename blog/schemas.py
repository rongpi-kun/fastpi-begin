from pydantic import BaseModel
from typing import List

class User(BaseModel):
    name: str
    email: str
    password: str

class BlogBase(BaseModel):
    title: str
    author: str

class Blog(BlogBase):
    class Config:
        orm_mode = True

class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog]

    class Config:
        orm_mode = True

class ShowBlog(BaseModel):
    title: str
    author: str
    creator: ShowUser
    
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True