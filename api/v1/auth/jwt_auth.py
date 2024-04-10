#!/usr/bin/env python3
from api.v1.views import app_views
import redis
from models import db, app
from models.user import User
from datetime import timedelta
from utils.pwd_hasher import PwdHasher
from flask_jwt_extended import create_access_token, JWTManager, jwt_required
from flask import (
                    request,
                    make_response,
                    abort,
                    jsonify
                  )


# provide strong secret key from env variable
app.config['JWT_SECRET_KEY'] = 'my secret'
ACCESS_EXPIRES = timedelta(hours=1)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = ACCESS_EXPIRES
jwt = JWTManager(app)

jwt_redis_blocklist = redis.StrictRedis(
    host='localhost', port=6379, db=2, decode_responses=True
)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None

@jwt.user_lookup_loader
def user_lookup_callback(jwt_header, jwt_data):
    identity = jwt_data['id']
    return User.query.filter_by(id=identity).first()

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    return make_response(jsonify({'message': redis_client.ping()}), 200)



@app_views.route('/auth/login', methods=['POST'], strict_slashes=False)
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username is None or password is None:
        abort(401)
    with app.app_context():
        user = db.one_or_404(db.select(User).filter_by(username=username))
    if not PwdHasher.pwd_check(password, user.password):
        abort(401)
    data = {'id': user.id}
    access_token = create_access_token(identity=username, additional_claims=data)
    return make_response(jsonify({'access_token': access_token}), 200)
