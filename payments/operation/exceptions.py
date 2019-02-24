"""
Operation exceptions
"""


class BaseOperationError(Exception):
    pass


class OperationDoesNotExistsError(BaseOperationError):

    def __init__(self):
        self.msg = "Operation not found"


class OperationInconsistentError(BaseOperationError):

    def __init__(self):
        self.msg = 'Operation inconsistent'
