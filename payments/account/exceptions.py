"""
Account exceptions
"""


class BaseAccountError(Exception):
    pass


class AccountAlreadyExistsError(BaseAccountError):

    def __init__(self):
        self.msg = 'Account already exists'


class AccountDoesNotExistsError(Exception):

    def __init__(self):
        self.msg = 'Account not found'
