class TransactionError(Exception):
    pass


class InvalidAmountError(TransactionError):
    pass


class UserNotFoundError(TransactionError):
    pass