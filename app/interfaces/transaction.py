from typing import Optional, Union
from app.interfaces import CustomBaseModel, CustomTimableModel
from app.interfaces.account import AccountInterface


class TransactionInterface(CustomTimableModel):
    transaction_id: Optional[int]
    account: Union[AccountInterface, int]
    amount: float
    transaction_type: int


class RequestDepositInterface(CustomBaseModel):
    account_id: int
    amount: float


class RequestWithdrawInterface(CustomBaseModel):
    account_id: int
    amount: float
