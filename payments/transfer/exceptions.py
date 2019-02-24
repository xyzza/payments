class BaseTransferError(Exception):
    pass


class InsufficientFundsError(BaseTransferError):

    def __init__(self):
        self.msg = 'Not enough funds to transfer'
