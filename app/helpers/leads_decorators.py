from functools import wraps
from http import HTTPStatus
from flask import request


def keys_verifier(func):

    @wraps(func)
    def wrapper():
        allowed_keys = ['email', 'name', 'phone']
        data: dict = request.get_json()

        try:
            for key in allowed_keys:
                if key not in data.keys():
                    raise KeyError

                if not type(data[key]) is str:
                    raise TypeError

            return func()

        except KeyError:

            return {
                'allowed_keys': allowed_keys,
                'received_keys': list(data.keys()),
            }, HTTPStatus.BAD_REQUEST

        except TypeError:
            return {
                'expected_types': {key: 'str'
                                   for key in allowed_keys},
                'received_types': {
                    key: f'{type(value).__name__}'
                    for key, value in data.items()
                }
            }, HTTPStatus.BAD_REQUEST

    return wrapper


def email_verifier(func):

    @wraps(func)
    def wrapper():
        data: dict = request.get_json()

        try:
            if 'email' not in data:
                raise KeyError
            if not type(data['email']) is str:
                raise TypeError
            return func()

        except KeyError:
            return {
                'allowed_keys': ['email'],
                'received_keys': list(data.keys())
            }, HTTPStatus.BAD_REQUEST
        except TypeError:
            return {
                'expected_types': {
                    'email': 'str'
                },
                'received_types': {
                    key: f'{type(value).__name__}'
                    for key, value in data.items()
                }
            }

    return wrapper