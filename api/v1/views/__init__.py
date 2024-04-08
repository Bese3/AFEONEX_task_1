#!/usr/bin/env python3
from flask import Blueprint

app_views = Blueprint('app', __name__, url_prefix='/api/v1')

from api.v1.views.user import *
from api.v1.auth.jwt_auth import *
from api.v1.views.post import *
from api.v1.views.comment import *