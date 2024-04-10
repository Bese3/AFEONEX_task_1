#!/usr/bin/env python3
import requests
import unittest
from models.user import User
from models import db, app
from utils.pwd_hasher import PwdHasher


api_status = False

try:
    if requests.get('http://localhost:5000/api/v1/status').json()['message'] == True:
        api_status = True
except Exception: 
    api_status = False


@unittest.skipIf(not api_status, 'cannot test when Server is down')
class TestUserAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        initializes class attributes for user data and adds two
        user instances to the database.
        """
        cls.first_name = 'abebe'
        cls.last_name = 'kebede'
        cls.username = 'test_username_user_api_1'
        cls.username_2 = 'test_username_user_api_2'
        cls.email = 'abebe@kebede2.com'
        cls.email_3 = 'abebe@kebede3.com'
        cls.password = PwdHasher.pwd_hash('pass123')
        phone = '0987452134'
        cls.uri = 'http://localhost:5000/api/v1/'
        cls.user_1 = User(first_name=cls.first_name, last_name=cls.last_name,
                    username=cls.username, email=cls.email, password=cls.password, phone=phone)
        cls.user_2 = User(first_name=cls.first_name, last_name=cls.last_name,
                    username=cls.username_2, email=cls.email_3, password=cls.password, phone='0989')
        with app.app_context():
            db.session.add(cls.user_1)
            db.session.add(cls.user_2)
            db.session.commit()

    @classmethod
    def tearDownClass(cls):
        """
        is used to clean up database session by deleting user objects.
        """
        with app.app_context():
            try:
                db.session.delete(cls.user_1)
                db.session.delete(cls.user_2)
                db.session.commit()
            except Exception:
                db.session.commit()

    def test_create_user_api(self):
        """
        tests the creation of a user via an API endpoint by sending
        a POST request with user data and verifying the response.
        """
        data = {
            'email': 'test_user_api_email@gmail.com',
            'first_name': 'test_user_api_fname',
            'last_name': 'test_user_api_lname',
            'password': 'pass123',
            'phone': 'test_user_api_1',
            'username': 'test_user_api_1'
        }
        headers = {
            'Content-Type': 'application/json'
        }
        with requests.post(self.uri + 'user/create', headers=headers) as response:
            self.assertEqual(response.status_code, 400)
            self.assertEqual(type(response.json()['message']), str)

        with requests.post(self.uri + 'user/create', headers=headers, json=data) as response:
            with app.app_context():
                test = db.one_or_404(db.select(User).filter_by(username=data['username']))
                db.session.delete(test)
                db.session.commit()
            self.assertEqual(response.status_code, 201)
            res_data = response.json()
            self.assertEqual(res_data['first_name'], data['first_name'])
            self.assertEqual(res_data['last_name'], data['last_name'])
            self.assertEqual(res_data['email'], data['email'])
            self.assertEqual(res_data['phone'], data['phone'])
            self.assertEqual(res_data['username'], data['username'])
            self.assertFalse(res_data['access_token'] is None)
            self.assertTrue(type(res_data['access_token']) == str)

    def test_user_update_api(self):
        """
        tests the user update API by simulating updating user
        data with different user tokens and checking for expected
        responses.
        """
        data_1 = {

            'password': 'pass123',
            'username': self.username
        }
        data_2 = {
             'password': 'pass123',
             'username': self.username_2
         }
        headers = {
            'Content-Type': 'application/json'
        }
        with app.app_context():
            user_1 = db.one_or_404(db.select(User).filter_by(username=data_1['username']))

        # logging in
        user_1_token = requests.post(self.uri + 'auth/login', json=data_1).json()
        user_2_token = requests.post(self.uri + 'auth/login', json=data_2).json()
        
        #  update user1 data logging as user1 must return the updated data
        headers['Authorization'] = f'Bearer {user_1_token["access_token"]}'
        with requests.put(self.uri + f'user/update/{user_1.id}',
                          headers=headers, json={'phone': '0678',
                                                 'password': 'pass1234'}) as res:
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json()['phone'], '0678')
            with app.app_context():
                u = db.one_or_404(db.select(User).filter_by(username=data_1['username']))
                self.assertTrue(PwdHasher.pwd_check('pass1234', u.password))

        # update user1 data logging as user2 must return 401 unauthorized
        headers['Authorization'] = f'Bearer {user_2_token["access_token"]}'
        with requests.put(self.uri + f'user/update/{user_1.id}',
                          headers=headers, json={'phone': '0678',
                                                 'password': 'pass1234'}) as res:
            self.assertEqual(res.status_code, 401)
            self.assertTrue(res.json()['message'] is not None)

    def test_user_delete_api(self):
        """
        tests the deletion of user data by logging in as different
        users and sending delete requests with appropriate
        authorization headers.
        """
        data_1 = {

            'password': 'pass123',
            'username': self.username
        }
        data_2 = {
             'password': 'pass123',
             'username': self.username_2
         }
        headers = {}
        with app.app_context():
            user_1 = db.one_or_404(db.select(User).filter_by(username=data_1['username']))
            user_2 = db.one_or_404(db.select(User).filter_by(username=data_2['username']))

        # logging in
        user_1_token = requests.post(self.uri + 'auth/login', json=data_1).json()
        user_2_token = requests.post(self.uri + 'auth/login', json=data_2).json()

        #  delete user1 data logging as user1 must return the deleted true
        headers['Authorization'] = f'Bearer {user_1_token["access_token"]}'
        with requests.delete(self.uri + f'user/delete/{user_1.id}',
                          headers=headers) as res:
             self.assertEqual(res.status_code, 200)

        headers['Authorization'] = f'Bearer {user_2_token["access_token"]}'
        with requests.delete(self.uri + f'user/delete/{user_2.id}',
                          headers=headers) as res:
             self.assertEqual(res.status_code, 200)

        TestUserAPI.setUpClass()

    def test_user_me_api(self):
        """
        tests API endpoint by logging in a user and checking
        if specific fields are present in the response.
        """
        data_1 = {

            'password': 'pass123',
            'username': self.username
        }
        headers = {}
        with app.app_context():
            user_1 = db.one_or_404(db.select(User).filter_by(username=data_1['username']))
        # logging in
        user_1_token = requests.post(self.uri + 'auth/login', json=data_1).json()
        headers['Authorization'] = f'Bearer {user_1_token["access_token"]}'
        with requests.get(self.uri + f'user/me/',
                          headers=headers) as res:
            self.assertEqual(res.status_code, 200)
            needed_fields = ['first_name', 'last_name', 'email', 'phone', 'username']
            for i in needed_fields:
                self.assertTrue(i in res.json().keys())
