from sqlalchemy import Column, Integer, String, Date, ForeignKey
from .database import Base
import datetime
from sqlalchemy.orm import relationship

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    blogs = relationship('BlogModel', back_populates='creator')

class BlogModel(Base):
    __tablename__ = 'blogs'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    published = Column(Date, default=datetime.date.today())
    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship('UserModel', back_populates='blogs')

