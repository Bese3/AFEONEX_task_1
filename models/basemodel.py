#!/usr/bin/env python3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from uuid import uuid4
from datetime import datetime
from sqlalchemy import String, Integer
from sqlalchemy.orm import (
                            DeclarativeBase,
                            # declarative_base,
                            Mapped,
                            mapped_column
                            )


# Base = declarative_base()
app = Flask(__name__)
# use env variables
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://twitt_dev:twitt_dev_pwd@localhost/twittBuzz_dev_db'


class BaseModel(DeclarativeBase):
    id: Mapped[str] = mapped_column(String(60), default=lambda: str(uuid4()), primary_key=True)
    created_at: Mapped[str] = mapped_column(String(60), default=lambda: (datetime.utcnow()))
    updated_at: Mapped[str] = mapped_column(String(60),
                                            default=lambda: (datetime.utcnow()), onupdate=lambda: (datetime.utcnow()))

db = SQLAlchemy(model_class=BaseModel)
db.init_app(app)
