from datetime import datetime
from peewee import (
    AutoField,
    CharField,
    DateTimeField
)
from app.database.provider import BaseModel
from playhouse.shortcuts import model_to_dict

from app.interfaces.account_owner import AccountOwnerInterface


class AccountOwnerEntity(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField()
    cpf = CharField(unique=True, max_length=11)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = "account_owner"

    def to_interface(self):
        fields = model_to_dict(self)
        return AccountOwnerInterface(**fields)
