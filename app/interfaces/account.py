from datetime import datetime

from app.config.enums.account import AccountStates
from app.interfaces import CustomBaseModel, CustomTimableModel

from typing import Optional, Union

from app.interfaces.account_owner import AccountOwnerInterface


class AccountInterface(CustomTimableModel):
    account_id: Optional[int]
    agency: Optional[str] = "0001"
    checking_account_number: int
    state: AccountStates = AccountStates.ACTIVE
    account_owner: Union[AccountOwnerInterface, int]
    updated_at: Optional[datetime]


class RequestCreateAccountInterface(CustomBaseModel):
    account_owner_id: int


class RequestBlockAccountInterface(CustomBaseModel):
    account_id: int