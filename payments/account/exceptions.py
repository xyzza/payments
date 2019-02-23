"""
Account exceptions
"""


class BaseAccountException(Exception):
    pass


class AccountAlreadyExists(BaseAccountException):

    def __init__(self):
        self.msg = 'Account already exists'


class AccountDoesNotExists(Exception):

    def __init__(self):
        self.msg = 'Account not found'
