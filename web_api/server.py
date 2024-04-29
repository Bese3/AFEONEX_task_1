#!/usr/bin/env python3

from flask import (
                    render_template,
                    jsonify,
                    make_response,
                    abort,
                    Flask,
                    request,
                    redirect,
                    url_for
                  )
from utils.memoize import Utility
from datetime import datetime
from models import app, db
from models.user import User
from flask_cors import CORS
import requests




app_view = Flask(__name__)
CORS(app_view, resources={r"/*": {"origins": "0.0.0.0"}})
uri = "http://localhost:5000/api/v1/"
auth_uri = f"{uri}auth/"


@app_view.route('/', methods=['GET'], strict_slashes=False)
@app_view.route('/home', methods=['GET'], strict_slashes=False)
def home():
    all_posts = requests.get(f"{uri}posts").json()
    all_posts = Utility.random_range_from_list(all_posts, len(all_posts))
    i = 0
    for post in all_posts:
        date = datetime.strptime(post['publication_date'], "%Y-%m-%d %H:%M:%S.%f")
        all_posts[i]['publication_date'] = Utility.format_datetime_ago(date)
        all_posts[i]['length'] = len(post['comments'])
        # print(post)
        with app.app_context():
            user = db.get_or_404(User, post['user_id'])
        all_posts[i]['username'] = user.username
        i += 1
    user = None
    try:
        cookies = request.cookies
        headers = {
            'Authorization': f"Bearer {cookies['access_token']}"
        }
        with requests.get(f"{auth_uri}check/user", headers=headers)as res:
            if res.status_code == 200:
                user = res.json()
    except Exception:
        pass
    return render_template('home.html', all_posts=all_posts, user=user)


@app_view.route('/auth/create-account', methods=['GET', "POST"], strict_slashes=False)
def create_account():
    user = None
    status = 0
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        data = request.get_json()
        try:
            with requests.post(f'{uri}user/create', json=data) as res:
                if res.status_code == 201:
                    user = res.json()
                    # return redirect(url_for('verify_email'))
                status = res.status_code
        except Exception:
            return jsonify({}), status
        return make_response(jsonify(user), 200)
    # elif request.method == 'PUT':


@app_view.route('/auth/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        data = request.get_json()
        if data['username'] is None or data['password'] is None:
            abort(400)
        token = None
        response = None
        with requests.post(f'{auth_uri}login', json=data) as res:
            if res.status_code == 200:
                res = res.json()
                token = res['access_token']
        if token:
            response = jsonify({'token': token})
        else:
            response = jsonify({'message': False})
            return response, 401
        return response, 200


@app_view.route('/post/<post_id>/<id>', methods=['GET'], strict_slashes=False)
def get_post(post_id, id):
    post = None
    user = None
    owner = None
    try:
        cookies = request.cookies
        headers = {
            'Authorization': f"Bearer {cookies['access_token']}"
        }
        with requests.get(f'{uri}post/{post_id}') as res:
            if res.status_code >= 400:
                return redirect(url_for('login'))
            elif res.status_code == 200:
                post = res.json()
        with requests.get(f"{auth_uri}check/user", headers=headers)as res:
            if res.status_code == 200:
                user = res.json()
            else:
                return redirect(url_for('login'))
        with requests.get(f"{uri}user/me/{id}") as res:
            if res.status_code == 200:
                owner = res.json()
            else:
                return redirect(url_for('login'))
    except Exception as e:
        # print(e)
        abort(401)
    date = datetime.strptime(post['publication_date'], "%Y-%m-%d %H:%M:%S.%f")
    post['publication_date'] = Utility.format_datetime_ago(date)
    post['length'] = len(post['comments'])
    i = 0
    for comment in post['comments']:
        com_date = datetime.strptime(comment['comment_date'], "%Y-%m-%d %H:%M:%S.%f")
        post['comments'][i]['comment_date'] = Utility.format_datetime_ago(com_date)
        with requests.get(f"{uri}user/me/{comment['commenter_id']}") as res:
            if res.status_code == 200:
                res = res.json()
                post['comments'][i]['commenter'] = f"{res['first_name']} {res['last_name']}"
                post['comments'][i]['username'] = res['username']
        i += 1
    return render_template('post.html', post=post, user=user, owner=owner)


@app_view.route('/post/<id>', methods=['POST'], strict_slashes=False)
def post(id):
    data = request.get_json()
    post = None
    try:
        cookies = request.cookies
        headers = {
            'Authorization': f"Bearer {cookies['access_token']}"
        }
        with requests.post(f'{uri}/post/create/{id}',
                           json=data, headers=headers) as res:
            if res.status_code == 201:
                post = res.json()
    except Exception:
        return jsonify({}), 401    
    return make_response(jsonify(post), 200)



@app_view.route('/comment/<post_id>', methods=['POST'], strict_slashes=False)
def create_comment(post_id):
    data = request.get_json()
    try:
        cookies = request.cookies
        headers = {
            'Authorization': f"Bearer {cookies['access_token']}"
        }
        with requests.post(f"{uri}comment/create/{post_id}",
                           json=data, headers=headers) as res:
            if res.status_code == 201:
                return jsonify({'message': True}), 200
            else:
                return jsonify({'message': False}), 400
    except Exception:
        return jsonify({'message': False}), 400


@app_view.route('/auth/verify-email', methods=['GET', 'POST'], strict_slashes=False)
def verify_email():
    if request.method == 'GET':
        return render_template('verify.html')
    if request.method == "POST":
        data = request.get_json()
        if Utility.verify_user(data['id'], data['otp']):
            return make_response(jsonify({'message': True}), 200)
        return make_response(jsonify({'message': False}), 200)





if __name__ == '__main__':
    app_view.run(host="0.0.0.0", port=5001, debug=True)
