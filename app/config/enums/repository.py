from enum import auto

from fastapi_utils.enums import StrEnum


class InFilterType(StrEnum):
    IN = auto()
    NOT_IN = auto()


class ReturnType(StrEnum):
    FIRST = auto()
    ALL = auto()
