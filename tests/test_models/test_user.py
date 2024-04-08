#!/usr/bin/env python3
import unittest
from models.user import User
from models.basemodel import db, app


class TestUser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.first_name = 'abebe'
        cls.last_name = 'kebede'
        cls.username = 'abekebe'
        cls.email = 'abebe@kebede.com'
        cls.password = '123pwd'
        phone = '0987452134'
        cls.user = User(first_name=cls.first_name, last_name=cls.last_name,
                    username=cls.username, email=cls.email, password=cls.password, phone=phone)
        with app.app_context():
            db.session.add(cls.user)
            db.session.commit()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.session.delete(cls.user)
            db.session.commit()
    

    def test_user_exists(self):
        '''
        user created in setup class exists in db
        '''
        with app.app_context():
            db.session.add(self.user)
            self.assertEqual(self.username, self.user.username)

    def test_email(self):
        '''
            Test that User has attr email
        '''
        with app.app_context():
            db.session.add(self.user)
            self.assertTrue(hasattr(self.user, "email"))
            self.assertEqual(self.user.email, self.email)

    def test_fName(self):
        '''
            Test that User has attr first_name
        '''
        with app.app_context():
            db.session.add(self.user)
            self.assertTrue(hasattr(self.user, "first_name"))
            self.assertEqual(self.user.first_name, self.first_name)

    def test_lName(self):
        '''
            Test that User has attr last_name
        '''
        with app.app_context():
            db.session.add(self.user)
            self.assertTrue(hasattr(self.user, "last_name"))
            self.assertEqual(self.user.last_name, self.last_name)
    
    def test_pwd(self):
        '''
            Test that User has attr password
        '''
        with app.app_context():
            db.session.add(self.user)
            self.assertTrue(hasattr(self.user, "password"))
            self.assertEqual(self.user.password, self.password)

        