#!/usr/bin/env python3
from models.basemodel import db, BaseModel
from typing import List
from sqlalchemy import String
from datetime import datetime
from sqlalchemy import ForeignKey
from models.comment import Comment
from sqlalchemy.orm import (
                            Mapped,
                            mapped_column,
                            relationship,
                            )


class Post(BaseModel, db.Model):
    __tablename__ = 'posts'
    user_id: Mapped[str] = mapped_column(String(60), ForeignKey('users.id'), nullable=False)
    author: Mapped[str] = mapped_column(String(60), nullable=False)
    publication_date: Mapped[str] = mapped_column(String(60),
                                                  default=str(datetime.utcnow()), onupdate=str(datetime.utcnow()))
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    body: Mapped[str] = mapped_column(String(2096), nullable=False)
    user = relationship('User', back_populates='posts')
    comments: Mapped[List['Comment']] = relationship(back_populates='post', cascade='all')
    