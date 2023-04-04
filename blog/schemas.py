from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    author: str
    published: str