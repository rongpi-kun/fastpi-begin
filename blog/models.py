from sqlalchemy import Column, Integer, String, Date
from .database import Base
import datetime

class BlogModel(Base):
    __tablename__ = 'blogs'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    published = Column(Date, default=datetime.date.today())

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)