class TransactionError(Exception):
    pass


class InvalidAmountError(TransactionError):
    pass


class InvalidTransactionReferenceError(TransactionError):
    pass


class AccountNotFoundError(TransactionError):
    pass


class InvalidStateDataError(TransactionError):
    pass


class UserNotFoundError(TransactionError):
    pass
