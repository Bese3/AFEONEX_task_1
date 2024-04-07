import unittest
from models.user import User


class TestUser(unittest.TestCase):
    def test_create_user(self):
        first_name = 'abebe'
        last_name = 'kebede'
        username = 'abekebe'
        email = 'abebe@kebede.com'
        password = '123pwd'
        phone = '0987452314'
        user = User(first_name=first_name, last_name=last_name,
                    username=username, email=email, password=password, phone=phone)
        self.assertEqual(True, False)
        