#!/usr/bin/env python3
from models.basemodel import db
from typing import List
from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import (
                            Mapped,
                            Column,
                            relationship
                            )


class User(db.Model):
    __tablename__ = 'users'
    first_name: Mapped[str] = Column(String(60), nullable=False)
    last_name: Mapped[str] = Column(String(60), nullable=False)
    username: Mapped[str] = Column(String(120), unique=True)
    email: Mapped[str] = Column(String(60), unique=True)
    password: Mapped[str] = Column(String(200), nullable=False)
    phone: Mapped[str] = Column(String(20), unique=True)
    post = relationship('Post', backref='users', cascade='all')


    def __repr__(self):
        '''
            return string representation of the user object
        '''
        return F'<User: firstName: {self.first_name}, email: {self.email}>'
