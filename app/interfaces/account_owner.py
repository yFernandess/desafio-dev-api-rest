

import re
from typing import Optional

from pydantic import validator
from app.interfaces import CustomBaseModel, CustomTimableModel


class AccountOwnerInterface(CustomTimableModel):
    id: Optional[int]
    name: str
    cpf: str

    @validator('cpf')
    def validate_cpf(cls, v):
        if not re.match(r'^\d{11}$', v):
            raise ValueError('CPF must contain only numbers and have 11 digits')
        return v


class RequestCreateAccountOwnerInterface(CustomBaseModel):
    name: str
    cpf: str

    @validator('cpf')
    def validate_cpf(cls, v):
        if not re.match(r'^\d{11}$', v):
            raise ValueError('CPF must contain only numbers and have 11 digits')
        return v


class RequestRemoveAccountOwnerInterface(CustomBaseModel):
    cpf: str

    @validator('cpf')
    def validate_cpf(cls, v):
        if not re.match(r'^\d{11}$', v):
            raise ValueError('CPF must contain only numbers and have 11 digits')
        return v
