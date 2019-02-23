"""
Operation exceptions
"""


class BaseOperationException(Exception):
    pass


class OperationDoesNotExists(BaseOperationException):

    def __init__(self):
        self.msg = "Operation not found"


class OperationInconsistent(BaseOperationException):

    def __init__(self):
        self.msg = 'Operation inconsistent'
