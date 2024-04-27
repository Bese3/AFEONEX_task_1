#!/usr/bin/env python3
from functools import wraps
import requests
from datetime import datetime
import jwt
from datetime import datetime, timedelta
import random

secret_key = 'my secret'


admin_user = {
    'first_name': 'admin',
    'last_name': 'admin',
    "email": "admin@gmail.com",
    "password": "pass123",
    "username": "admin",
    "phone": "0912452317"
}

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


class reqstAdmin:
    @memoize
    def get_admin(self):
        return requests.post('http://localhost/api/v1/user/create', json=admin_user).json()

    @staticmethod
    def is_token_valid(token):
        try:
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            # Check expiration
            if 'exp' in payload:
                current_time = datetime.utcnow()
                if current_time > datetime.utcfromtimestamp(payload['exp']):
                    return False  # Token has expired
            # Signature verification (optional but recommended)
            # jwt.decode() will raise an exception if the signature is invalid
            jwt.decode(token, secret_key, algorithms=['HS256'])
            return True  # Token is valid
        except jwt.ExpiredSignatureError:
            return False  # Token has expired
        except jwt.InvalidTokenError:
            return False 