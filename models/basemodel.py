#!/usr/bin/env python3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from uuid import uuid4
from datetime import datetime
from sqlalchemy import String, Integer
from sqlalchemy.orm import (
                            DeclarativeBase,
                            Mapped,
                            mapped_column
                            )


app = Flask(__name__)
# use env variables
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://twitt_dev:twitt_dev_pwd@localhost/twittBuzz_dev_db'


class BaseModel(DeclarativeBase):
    id: Mapped[str] = mapped_column(String(60), default=str(uuid4()), primary_key=True)
    created_at: Mapped[str] = mapped_column(String(60), default=str(datetime.utcnow()))
    updated_at: Mapped[str] = mapped_column(String(60),
                                            default=str(datetime.utcnow()), onupdate=str(datetime.utcnow()))

db = SQLAlchemy(model_class=BaseModel)
db.init_app(app)