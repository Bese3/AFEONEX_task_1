#!/usr/bin/env python3

from api.v1.views import app_views
from models.user import User
from models import db, app
from utils.pwd_hasher import PwdHasher
from api.v1.auth.jwt_auth import jwt_required
from flask_jwt_extended import get_current_user, create_access_token
from flask import (
                    request,
                    make_response,
                    jsonify,
                    abort
                  )


@app_views.route('/user/create', methods=['POST'], strict_slashes=False)
def create_user():
    """
    creates a new user in a database, hashes the password, and
    returns user information along with an access token.
    """
    if not request.json:
        abort(404)
    allowed_fields = ['first_name', 'last_name', 'username', 'email', 'password', 'phone']
    for field in allowed_fields:
        if field not in request.json:
            abort(404)
    data = request.get_json()
    data['password'] = PwdHasher.pwd_hash(data['password'])
    user = User(**data)
    if user is None:
        abort(404)
    with app.app_context():
        db.session.add(user)
        db.session.commit()
        user = db.get_or_404(User, user.id)
    # redaction needed for email and password
    # and email verification needed
    data = {'id': user.id}
    access_token = create_access_token(identity=user.username, additional_claims=data)
    return make_response(jsonify({'first_name': user.first_name,
                                  'last_name': user.last_name,
                                  'username': user.username,
                                  'email': user.email,
                                  'phone': user.phone,
                                  'access_token': access_token}), 201)


@app_views.route('/user/update/<id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_user(id):
    """
    updates user information based on the provided fields in a JSON
    request, with certain validation checks and database operations.
    """
    current_user = get_current_user()
    if current_user.id != id:
        abort(401)
    if not request.json:
        abort(404)
    allowed_fields = ['first_name', 'last_name', 'username', 'email', 'password', 'phone']
    for field in request.json:
        if field not in allowed_fields:
            abort(404)
    data = request.get_json()
    with app.app_context():
        user = db.get_or_404(User, id)
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'username' in data:
            user.username = data['username']
        # email verification needed
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.password = data['password']
        if 'phone' in data:
            user.phone = data['phone']
        db.session.commit()
        user = db.get_or_404(User, id)

    return make_response(jsonify({'first_name': user.first_name,
                                  'last_name': user.last_name,
                                  'username': user.username,
                                  'email': user.email,
                                  'phone': user.phone}), 200)


@app_views.route('/user/delete/<id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_user(id):
    """
    deletes a user from the database after checking
    authorization and request validity.
    """
    current_user = get_current_user()
    if current_user.id != id:
        abort(401)
    if not request.json:
        abort(404)
    if not id:
        abort(404)
    with app.app_context():
        user = db.get_or_404(User, id)
        db.session.delete(user)
        db.session.commit()
    return make_response(jsonify({'deleted': True}), 200)
