#!/usr/bin/env python3

from api.v1.views import app_views
from models.post import Post
from models import db, app
from api.v1.auth.jwt_auth import jwt_required
from flask_jwt_extended import get_current_user, get_jwt_identity
from flask import (
                    request,
                    make_response,
                    jsonify,
                    abort
                  )


@app_views.route('/post/create/<id>', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_post(id):
    """
    creates a new post with specified fields and adds it to the database,
    returning a response with the post details and associated comments.
    """
    current_user = get_current_user()
    if current_user.id != id:
        abort(401)
    if not request.json:
        abort(400)
    allowed_fields = ['body']
    for field in allowed_fields:
        if field not in request.json:
            abort(400)
    if 'author' not in request.json:
        request.json['author'] = current_user.first_name + ' ' + current_user.last_name
    data = request.get_json()
    data['user_id'] = id
    post = Post(**data)
    if post is None:
        abort(404)
    with app.app_context():
        db.session.add(post)
        db.session.commit()
        post = db.get_or_404(Post, post.id)
        all_comments = post.comments
        comments = [
                    {
                        'message': c.message, 
                        'comment_date': c.comment_date,
                        'commenter_id': c.commenter_id, 
                        'post_id': c.post_id} for c in all_comments]

    return make_response(jsonify({'title': post.title,
                                  'author': post.author,
                                  'comments': comments,
                                  'body': post.body,
                                  'id': post.id}), 201)


@app_views.route('/post/update/<id>/<post_id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_post(id, post_id):
    """
    updates a post with specified fields and returns the updated post details
    along with its comments.
    """
    current_user = get_current_user()
    if current_user.id != id:
        abort(401)
    if not request.json:
        abort(404)
    allowed_fields = ['body', 'author']
    for field in request.json:
        if field not in allowed_fields:
            abort(404)
    data = request.get_json()
    with app.app_context():
        post = db.get_or_404(Post, post_id)
        if current_user.id != post.user_id:
            abort(401)
        if 'title' in data:
            post.title = data['title']
        if 'body' in data:
            post.body = data['body']
        if 'author' in data:
            post.author = data['author']
        db.session.commit()
        post = db.get_or_404(Post, post_id)
        all_comments = post.comments
        comments = [
                    {
                        'message': c.message, 
                        'comment_date': c.updated_at,
                        'commenter_id': c.commenter_id, 
                        'post_id': c.post_id} for c in all_comments]

    return make_response(jsonify({'title': post.title,
                                  'body': post.body,
                                  'author': post.author,
                                  'comments': comments,
                                  'publication_date': post.updated_at,
                                  'id': post.id}), 200)


@app_views.route('/post/delete/<id>/<post_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_post(id, post_id):
    """
    deletes a post based on the provided post ID
    after checking the current user's authorization.
    """
    current_user = get_current_user()
    if current_user.id != id:
        abort(401)
    with app.app_context():
        post = db.get_or_404(Post, post_id)
        if current_user.id != post.user_id:
            abort(401)
        db.session.delete(post)
        db.session.commit()
    return make_response(jsonify({'deleted': True}), 200)


@app_views.route('/post/<post_id>', methods=['GET'], strict_slashes=False)
def get_post(post_id):
    with app.app_context():
        post = db.one_or_404(db.select(Post).filter_by(id=post_id))
        all_comments = post.comments
        comments = [
                    {
                        'message': c.message, 
                        'comment_date': c.updated_at,
                        'commenter_id': c.commenter_id, 
                        'post_id': c.post_id} for c in all_comments]
        # print(post.publication_date)

    return make_response(jsonify({'title': post.title,
                                  'body': post.body,
                                  'author': post.author,
                                  'comments': comments,
                                  'publication_date': post.updated_at,
                                  'id': post.id}), 200)


@app_views.route('/post/<id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_all_user_posts(id):
    user = get_current_user()
    if user.id != id:
        abort(401)
    with app.app_context():
        all_posts = [p for p in user.posts if p.user_id == user.id]
        i = 0
        for post in all_posts:
            comments = [{
                            'message': c.message, 
                            'comment_date': c.updated_at,
                            'commenter_id': c.commenter_id, 
                            'post_id': c.post_id} for c in post.comments]
            post_dict = {'title': post.title,
                                  'body': post.body,
                                  'author': post.author,
                                  'comments': comments,
                                  'publication_date': post.updated_at,
                                  'id': post.id}
            
            all_posts[i] = post_dict
            i += 1
            # print(all_posts[i - 1])

    return make_response(jsonify(all_posts), 200)


@app_views.route('/posts', methods=['GET'], strict_slashes=False)
def get_all_posts():
    with app.app_context():
        all_posts = Post.query.all()
        i = 0
        for post in all_posts:
            comments = [{
                            'message': c.message, 
                            'comment_date': c.updated_at,
                            'commenter_id': c.commenter_id, 
                            'post_id': c.post_id} for c in post.comments]
            post_dict = {'title': post.title,
                                  'body': post.body,
                                  'author': post.author,
                                  'comments': comments,
                                  'publication_date': post.updated_at,
                                  'id': post.id,
                                  'user_id': post.user_id}
            
            all_posts[i] = post_dict
            i += 1
            # print(all_posts[i - 1])

    return make_response(jsonify(all_posts), 200)
