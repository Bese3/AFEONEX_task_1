#!/usr/bin/env python3
import requests
import unittest
from models.post import Post
from models.comment import Comment
from models.user import User
from models import db, app
from utils.pwd_hasher import PwdHasher
from tests.test_api.test_user_api import api_status


@unittest.skipIf(not api_status, 'cannot test when Server is down')
class TestCommentAPI(unittest.TestCase):
    @classmethod
    def setUp(cls):
        """
        initializes class attributes for user data and adds two
        user instances to the database.
        """
        cls.first_name = 'abebe'
        cls.last_name = 'kebede'
        cls.username = 'test_username_user_api_5'
        cls.username_2 = 'test_username_user_api_6'
        cls.email = 'abebe@kebede6.com'
        cls.email_3 = 'abebe@kebede7.com'
        cls.password = PwdHasher.pwd_hash('pass123')
        cls.title = 'new title'
        cls.body = 'new body'
        cls.message = 'new comment'
        phone = '0987452144'
        cls.uri = 'http://localhost:5000/api/v1/'
        cls.user_1 = User(first_name=cls.first_name, last_name=cls.last_name,
                    username=cls.username, email=cls.email, password=cls.password, phone=phone)
        cls.user_2 = User(first_name=cls.first_name, last_name=cls.last_name,
                    username=cls.username_2, email=cls.email_3, password=cls.password, phone='0999')
        with app.app_context():
            db.session.add(cls.user_1)
            db.session.add(cls.user_2)
            db.session.commit()
            cls.post_1 = Post(user_id=cls.user_1.id,
                              author=cls.user_1.first_name,
                              title=cls.title, body=cls.body)
            cls.post_2 = Post(user_id=cls.user_2.id,
                              author=cls.user_2.first_name,
                              title=cls.title, body=cls.body)
            db.session.add(cls.post_1)
            db.session.add(cls.post_2)
            db.session.commit()
            cls.comment_1 = Comment(user_id=cls.user_1.id,
                                  post_id=cls.post_1.id,
                                  message=cls.message,
                                  commenter_id=cls.user_1.id)
            cls.comment_2 = Comment(user_id=cls.user_2.id,
                                  post_id=cls.post_2.id,
                                  message=cls.message,
                                  commenter_id=cls.user_2.id)
            db.session.add(cls.comment_1)
            db.session.add(cls.comment_2)
            db.session.commit()

    @classmethod
    def tearDown(cls):
        """
        is used to clean up database session by deleting user objects.
        """
        with app.app_context():
            try:
                db.session.delete(cls.user_1)
                db.session.delete(cls.user_2)
                db.session.commit()
            except Exception:
                pass
            try:
                db.session.delete(cls.post_1)
                db.session.delete(cls.post_2)
                db.session.commit()
            except Exception:
                pass
            try:
                db.session.delete(cls.comment_1)
                db.session.delete(cls.comment_2)
                db.session.commit()
            except Exception:
                pass

    def test_comment_create_api(self):
        data = {
            'message': 'test message'
        }
        # logging in
        login_data = {

            'password': 'pass123',
            'username': self.username
        }
        headers = {
            'Content-Type': 'application/json'
        }
        user_1_token = requests.post(self.uri + 'auth/login', json=login_data).json()
        headers['Authorization'] = f'Bearer {user_1_token["access_token"]}'
        # creating post
        with app.app_context():
            db.session.add(self.user_1)
            db.session.add(self.post_1)
            with requests.post(self.uri + f'comment/create/{self.user_1.id}/{self.post_1.id}',
                            json=data, headers=headers) as res:
                self.assertEqual(res.status_code, 201)

    # def test_comment_update_api(self):
    #     data_1 = {

    #         'password': 'pass123',
    #         'username': self.username
    #     }
    #     data_2 = {
    #          'password': 'pass123',
    #          'username': self.username_2
    #      }
    #     headers = {
    #         'Content-Type': 'application/json'
    #     }
    #     with app.app_context():
    #         db.session.add(self.post_1)
    #         user_1 = db.one_or_404(db.select(User).filter_by(username=data_1['username']))
    #         user_2 = db.one_or_404(db.select(User).filter_by(username=data_2['username']))
    #         post_1 = db.one_or_404(db.select(Post).filter_by(id=self.post_1.id))
    #         post_2 = db.one_or_404(db.select(Post).filter_by(id=self.post_2.id))


    #     # logging in
    #     user_1_token = requests.post(self.uri + 'auth/login', json=data_1).json()
    #     user_2_token = requests.post(self.uri + 'auth/login', json=data_2).json()
    #     headers['Authorization'] = f'Bearer {user_1_token["access_token"]}'
    #     # should update the post
    #     with requests.put(self.uri + f'comment/update/{post_1.id}',
    #                       headers=headers, json={
    #                           'title': 'updated title',
    #                           'body': 'updated body'
    #                       }) as res:
    #         self.assertEqual(res.status_code, 200)
    #         self.assertEqual(res.json()['title'], 'updated title')
    #         self.assertEqual(res.json()['body'], 'updated body')
    #     headers['Authorization'] = f'Bearer {user_2_token["access_token"]}'
    #     # should return 401 unauthorized
    #     with requests.put(self.uri + f'post/update/{user_1.id}/{post_1.id}',
    #                       headers=headers, json={
    #                           'title': 'updated title',
    #                           'body': 'updated body'
    #                       }) as res:
    #         self.assertEqual(res.status_code, 401)
    #         self.assertTrue(res.json()['message'] is not None)
    #         self.assertTrue(type(res.json()['message']) is str)

    # def test_post_delete_api(self):
    #     data_1 = {

    #         'password': 'pass123',
    #         'username': self.username
    #     }
    #     data_2 = {
    #          'password': 'pass123',
    #          'username': self.username_2
    #      }
    #     headers = {}
    #     with app.app_context():
    #         db.session.add(self.post_1)
    #         db.session.add(self.post_2  )
    #         user_1 = db.one_or_404(db.select(User).filter_by(username=data_1['username']))
    #         user_2 = db.one_or_404(db.select(User).filter_by(username=data_2['username']))
    #         post_1 = db.one_or_404(db.select(Post).filter_by(id=self.post_1.id))
    #         post_2 = db.one_or_404(db.select(Post).filter_by(id=self.post_2.id))


    #     # logging in
    #     user_1_token = requests.post(self.uri + 'auth/login', json=data_1).json()
    #     user_2_token = requests.post(self.uri + 'auth/login', json=data_2).json()
    #     headers['Authorization'] = f'Bearer {user_1_token["access_token"]}'
    #     # should update the post
    #     with requests.delete(self.uri + f'post/delete/{user_1.id}/{post_1.id}',
    #                       headers=headers) as res:
    #         self.assertEqual(res.status_code, 200)
    #         self.assertEqual(res.json()['deleted'], True)
    #     headers['Authorization'] = f'Bearer {user_2_token["access_token"]}'
    #     # should return 401 unauthorized
    #     with requests.delete(self.uri + f'post/delete/{user_1.id}/{post_1.id}',
    #                       headers=headers) as res:
    #         self.assertEqual(res.status_code, 401)
    #         self.assertTrue(res.json()['message'] is not None)
    #         self.assertTrue(type(res.json()['message']) is str)
        
    #     with requests.delete(self.uri + f'post/delete/{user_2.id}/{post_2.id}',
    #                       headers=headers) as res:
    #         self.assertEqual(res.status_code, 200)
    #         self.assertEqual(res.json()['deleted'], True)
