from starlette import status

from app.interfaces.exceptions import ExceptionInterface


class ExceptionMessageBuilder(Exception):
    def __init__(self, ex_info: ExceptionInterface):
        self.title = ex_info.title
        self.status_code = ex_info.status_code
        self.message = ex_info.message


class ObjectNotFound(ExceptionMessageBuilder):
    def __init__(self, ex_info: ExceptionInterface = None, object_name: str = ""):
        ex_info = ex_info or ExceptionInterface(
            title="Object " + object_name + " not found",
            message="Account not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
        super(ObjectNotFound, self).__init__(ex_info=ex_info)


class InsufficientBalance(ExceptionMessageBuilder):
    def __init__(self, ex_info: ExceptionInterface = None, object_name: str = ""):
        ex_info = ex_info or ExceptionInterface(
            title="Insufficient balance",
            message="Insufficient balance for this transaction",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
        super(InsufficientBalance, self).__init__(ex_info=ex_info)


class TransactionNotAllowed(ExceptionMessageBuilder):
    def __init__(self, ex_info: ExceptionInterface = None, object_name: str = ""):
        ex_info = ex_info or ExceptionInterface(
            title="Transaction not allowed",
            message="Transaction allowed for active accounts only.",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
        super(TransactionNotAllowed, self).__init__(ex_info=ex_info)


class DailyLimitReached(ExceptionMessageBuilder):
    def __init__(self, ex_info: ExceptionInterface = None, object_name: str = ""):
        ex_info = ex_info or ExceptionInterface(
            title="Daily limit reached",
            message="Daily limit reached for this account",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
        super(DailyLimitReached, self).__init__(ex_info=ex_info)
