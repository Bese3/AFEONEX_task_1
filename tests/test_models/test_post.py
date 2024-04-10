#!/usr/bin/env  python3
import unittest
from models.user import User
from models.post import Post
from models.basemodel import db, app
from datetime import datetime


class TestPost(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.first_name = 'abebe'
        cls.last_name = 'kebede'
        cls.username = 'test_username_post'
        cls.email = 'kebede@abebe.com'
        cls.password = '123pwd'
        phone = '0987452314'
        cls.user = User(first_name=cls.first_name, last_name=cls.last_name,
                        username=cls.username, email=cls.email, password=cls.password, phone=phone)
        with app.app_context():
            db.session.add(cls.user)
            db.session.commit()

        cls.author = cls.first_name + ' ' + cls.last_name
        cls.title = 'test title'
        cls.body = 'test body'
        with app.app_context():
            db.session.add(cls.user)
            cls.post = Post(user_id=cls.user.id, author=cls.author, title=cls.title, body=cls.body)
            db.session.add(cls.post)
            db.session.commit()
        

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.session.delete(cls.user)
            db.session.commit()
    

    def test_post_exists(self):
        '''
        post created in setup class exists in db
        '''
        with app.app_context():
            db.session.add(self.user)
            db.session.add(self.post)
            self.assertFalse(self.post is None)

    def test_post_user_id(self):
        '''
            created post user id
        '''
        with app.app_context():
            db.session.add(self.user)
            db.session.add(self.post)
            self.assertTrue(hasattr(self.post, 'user_id'))
            self.assertEqual(self.post.user_id, self.user.id)

    def test_post_author(self):
        '''
            created post author
        '''
        with app.app_context():
            db.session.add(self.user)
            db.session.add(self.post)
            self.assertTrue(hasattr(self.post, 'author'))
            self.assertFalse(self.post.author is None)
            self.assertEqual(self.post.author, self.first_name + ' ' + self.last_name)

    def test_post_title(self):
        '''
            created post title
        '''
        with app.app_context():
            db.session.add(self.user)
            db.session.add(self.post)
            self.assertTrue(hasattr(self.post, 'title'))
            self.assertFalse(self.post.title is None)

    def test_post_user(self):
        '''
        created user has the post
        '''
        with app.app_context():
            db.session.add(self.user)
            db.session.add(self.post)
            for post in self.user.posts:
                self.assertEqual(post.id, self.post.id)
                self.assertEqual(self.post.title, post.title)

    def test_post_body(self):
        '''
            created post body
        '''
        with app.app_context():
            db.session.add(self.user)
            db.session.add(self.post)
            self.assertTrue(hasattr(self.post, 'body'))
            self.assertFalse(self.post.body is None)

    def test_post_timestamp(self):
        'checks timestamps'
        with app.app_context():
            db.session.add(self.user)
            db.session.add(self.post)
            self.assertTrue(hasattr(self.post, 'created_at'))
            self.assertTrue(hasattr(self.post, 'updated_at'))
            self.assertTrue(type(self.post.created_at) is str)
            self.assertTrue(type(self.post.updated_at) is str)
            time = "%Y-%m-%d %H:%M:%S.%f"
            created_at = datetime.strptime(self.post.created_at, time)
            self.assertTrue(type(created_at) is datetime)
            updated_at = datetime.strptime(self.post.updated_at, time)
            self.assertTrue(type(updated_at) is datetime)
            self.assertTrue(updated_at > created_at)
