#!/usr/bin/env python3
from models.basemodel import db, BaseModel
from sqlalchemy import String
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
                            Mapped,
                            mapped_column,
                            relationship
                            )


class Comment(BaseModel, db.Model):
    __tablename__ = 'comments'
    user_id: Mapped[str] = mapped_column(String(60), ForeignKey('users.id'), nullable=False)
    post_id: Mapped[str] = mapped_column(String(60), ForeignKey('posts.id'), nullable=False)
    message: Mapped[str] = mapped_column(String(1048), nullable=False)
    comment_date: Mapped[str] = mapped_column(String(60),
                                                  default=str(datetime.utcnow()), onupdate=str(datetime.utcnow()))
    post = relationship('Post', back_populates='comments')
