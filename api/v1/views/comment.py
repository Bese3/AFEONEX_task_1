#!/usr/bin/env python3

from api.v1.views import app_views
from models.comment import Comment
from models.post import Post
from models import db, app
from api.v1.auth.jwt_auth import jwt_required
from flask_jwt_extended import get_current_user
from flask import (
                    request,
                    make_response,
                    jsonify,
                    abort
                  )


@app_views.route('/comment/create/<post_id>', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_comment(post_id):
    """
    creates a new comment associated with a specific user and post, and
    returns the comment details in JSON format.
    """
    current_user = get_current_user()
    if not request.json:
        abort(400)
    allowed_fields = ['message']
    for field in allowed_fields:
        if field not in request.json:
            abort(400)
    data = request.get_json()
    with app.app_context():
        post = db.one_or_404(db.select(Post).filter_by(id=post_id))
    data['user_id'] = post.user_id
    data['post_id'] = post_id
    data['commenter_id'] = current_user.id
    comment = Comment(**data)
    if comment is None:
        abort(400)
    with app.app_context():
        db.session.add(comment)
        db.session.commit()
        comment = db.get_or_404(Comment, comment.id)
    return make_response(jsonify({'message': comment.message,
                                  'comment_date': comment.created_at,
                                  'post_id': comment.post_id}), 201)


@app_views.route('/comment/update/<comment_id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_comment(comment_id):
    """
    updates a comment with a new message and returns the updated comment
    details in a JSON response.
    """
    current_user = get_current_user()
    # if current_user.id != id:
    #     abort(401)
    if not request.json:
        abort(400)
    allowed_fields = ['message']
    for field in request.json:
        if field not in allowed_fields:
            abort(400)
    data = request.get_json()
    with app.app_context():
        comment = db.get_or_404(Comment, comment_id)
        if comment.commenter_id != current_user.id:
            abort(401)
        if 'message' in data:
            comment.message = data['message']
        db.session.commit()
        comment = db.get_or_404(Comment, comment_id)

    return make_response(jsonify({'message': comment.message,
                                  'comment_date': comment.updated_at,
                                  'post_id': comment.post_id}), 200)


@app_views.route('/comment/delete/<id>/<comment_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_comment(id, comment_id):
    """
    deletes a specific comment if the current user is authorized and the
    request is valid.
    """
    current_user = get_current_user()
    if current_user.id != id:
        abort(401)
    if not request.json:
        abort(404)
    if not id:
        abort(404)
    with app.app_context():
        comment = db.get_or_404(Comment, comment_id)
        if comment.commenter_id != current_user.id:
            abort(401)
        db.session.delete(comment)
        db.session.commit()
    return make_response(jsonify({'deleted': True}), 200)
