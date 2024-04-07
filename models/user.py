#!/usr/bin/env python3
from models.basemodel import db, BaseModel
from typing import List
from sqlalchemy import String
from models.post import Post
from sqlalchemy.orm import (
                            Mapped,
                            mapped_column,
                            relationship
                            )


class User(BaseModel, db.Model):
    __tablename__ = 'users'
    first_name: Mapped[str] = mapped_column(String(60), nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)
    username: Mapped[str] = mapped_column(String(120), unique=True)
    email: Mapped[str] = mapped_column(String(60), unique=True)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), unique=True)
    posts: Mapped[List['Post']] = relationship('Post', back_populates='user', cascade='all')


    def __repr__(self):
        '''
            return string representation of the user object
        '''
        return F'<User: firstName: {self.first_name}, email: {self.email}>'
