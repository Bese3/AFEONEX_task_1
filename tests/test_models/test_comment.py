#!/usr/bin/env python3
import unittest
from models.user import User
from models.post import Post
from models.comment import Comment
from models.basemodel import db, app
from datetime import datetime
from uuid import uuid4


class TestComment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.first_name = 'abebe'
        cls.last_name = 'kebede'
        cls.username = 'test_username_comment'
        cls.email = 'kebe@abebe.com'
        cls.password = '123pwd'
        phone = '0987542314'
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
        
        cls.message = 'test comment'
        with app.app_context():
            db.session.add(cls.user)
            db.session.add(cls.post)
            cls.comment = Comment(message=cls.message, user_id=cls.user.id, post_id=cls.post.id, commenter_id=str(uuid4()))
            db.session.add(cls.comment)
            db.session.commit()
        

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.session.delete(cls.user)
            db.session.commit()
    

    def test_comment_exists(self):
        '''
        post created in setup class exists in db
        '''
        with app.app_context():
            db.session.add(self.user)
            db.session.add(self.post)
            print(self.comment)
            db.session.add(self.comment)
            self.assertFalse(self.comment is None)

    def test_comment_user_id_post_id(self):
        '''
            created comment user id and post id
        '''
        with app.app_context():
            db.session.add(self.user)
            db.session.add(self.post)
            db.session.add(self.comment)
            self.assertTrue(hasattr(self.comment, 'user_id'))
            self.assertEqual(self.post.user_id, self.user.id)
            self.assertTrue(hasattr(self.comment, 'post_id'))
            self.assertEqual(self.comment.post_id, self.post.id)

    def test_comment_message(self):
        '''
            created comment message
        '''
        with app.app_context():
            db.session.add(self.user)
            db.session.add(self.post)
            db.session.add(self.comment)
            self.assertTrue(hasattr(self.comment, 'message'))
            self.assertFalse(self.comment.message is None)

    def test_comment_timestamp(self):
        'checks timestamps'
        with app.app_context():
            db.session.add(self.user)
            db.session.add(self.post)
            db.session.add(self.comment)
            self.assertTrue(hasattr(self.comment, 'created_at'))
            self.assertTrue(hasattr(self.comment, 'updated_at'))
            self.assertTrue(type(self.comment.created_at) is str)
            self.assertTrue(type(self.comment.updated_at) is str)
            time = "%Y-%m-%d %H:%M:%S.%f"
            created_at = datetime.strptime(self.comment.created_at, time)
            self.assertTrue(type(created_at) is datetime)
            updated_at = datetime.strptime(self.comment.updated_at, time)
            self.assertTrue(type(updated_at) is datetime)
            self.assertTrue(updated_at > created_at)

    def test_comment_user(self):
        '''
            checks if user contain the comment
        '''
        with app.app_context():
            db.session.add(self.user)
            db.session.add(self.post)
            db.session.add(self.comment)
            comment = self.user.posts[0].comments[0]
            self.assertEqual(comment.id, self.comment.id)
            self.assertEqual(comment.user_id, self.user.id)
            self.assertEqual(comment.post_id, self.post.id)
