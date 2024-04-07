#!/usr/bin/env python3
from basemodel import db
from typing import List
from sqlalchemy import String
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
                            Mapped,
                            mapped_column,
                            relationship
                            )


class Post(db.Model):
    __tablename__ = 'posts'
    user_id: Mapped[str] = mapped_column(String(60), ForeignKey('users.id'), nullable=False)
    author: Mapped[str] = mapped_column(String(60), nullable=False)
    publication_date: Mapped[str] = mapped_column(String(60),
                                                  default=datetime.utcnow, onupdate=datetime.utcnow)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    body: Mapped[str] = mapped_column(String(2096), nullable=False)
    comment: Mapped[List['comments']] = relationship(back_populates='posts')
