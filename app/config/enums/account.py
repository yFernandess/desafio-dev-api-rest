from fastapi_utils.enums import StrEnum
from enum import auto


class AccountStates(StrEnum):
    ACTIVE = auto()
    BLOCKED = auto()
    CLOSED = auto()
