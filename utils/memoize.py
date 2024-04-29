#!/usr/bin/env python3
from functools import wraps
import requests
from datetime import datetime
import jwt
from datetime import datetime
import random, redis

# secret_key = 'my secret'

r = redis.Redis(host='localhost', port=6379, db=0)


def memoize(fn):
    attr_name = 'data'

    @wraps(fn)
    def memoized(self):
        if not hasattr(self, attr_name):
            print('check')
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return property(memoized)


class Utility:
    @staticmethod
    def random_range_from_list(input_list, range_size):
        if len(input_list) <= range_size:
            return input_list  # If the list size is smaller than or equal to the desired range, return the entire list
        
        start_index = random.randint(0, len(input_list) - range_size)
        end_index = start_index + range_size
        
        return input_list[start_index:end_index]

    @staticmethod
    def format_datetime_ago(post_datetime):
        current_datetime = datetime.now()
        time_difference = current_datetime - post_datetime
        # Calculate the difference in seconds
        seconds_difference = time_difference.total_seconds()
        # print(f"{time_difference} = {current_datetime} - {post_datetime}")

        # Define time intervals in seconds
        intervals = {
            'year': 31536000,
            'month': 2592000,
            'week': 604800,
            'day': 86400,
            'hour': 3600,
            'minute': 60
        }

        # Iterate over intervals to find the appropriate time unit
        for unit, value in intervals.items():
            if seconds_difference >= value:
                num_units = int(seconds_difference / value)
                return f"{num_units} {unit}{'s' if num_units > 1 else ''} ago"

        # If the post is less than a minute old
        return "Just now"

    @staticmethod
    def key_setter(key, value, time=600):
        if key is None or value is None:
            raise ValueError('key or value is None')
        r.setex(key, time, value)
        return True

    @staticmethod
    def value_getter(key):
        if key is None:
            raise ValueError('key is None')
        return r.get(key)

    @staticmethod
    def verify_user(id, user_input):
        key = f'auth_{id}'
        try:
            value = Utility.value_getter(key)
            print(f'value = {value}, user_input = {user_input}')
            if int(value) == int(user_input):
                return True
        except ValueError:
            return False
        return False

class reqstAdmin:
    admin_user = {
    'first_name': 'admin',
    'last_name': 'admin',
    "email": "admin@gmail.com",
    "password": "pass123",
    "username": "admin",
    "phone": "0912452317"
}
    @memoize
    def get_admin(self):
        return requests.post('http://localhost/api/v1/user/create', json=self.admin_user).json()
