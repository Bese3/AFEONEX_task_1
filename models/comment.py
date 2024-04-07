#!/usr/bin/env python3
from basemodel import db
from sqlalchemy import String
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
                            Mapped,
                            mapped_column
                            )


class Comment(db.Model):
    __tablename__ = 'comments'
    user_id: Mapped[str] = mapped_column(String(60), ForeignKey('users.id'), nullable=False)
    post_id: Mapped[str] = mapped_column(String(60), ForeignKey('posts.id'), nullable=False)
    message: Mapped[str] = mapped_column(String(1048), nullable=False)
    comment_date: Mapped[str] = mapped_column(String(60),
                                                  default=datetime.utcnow, onupdate=datetime.utcnow)
