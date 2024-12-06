from datetime import datetime
from peewee import (
    AutoField,
    ForeignKeyField,
    CharField,
    IntegerField,
    DateTimeField,
    DecimalField,
)
from playhouse.shortcuts import model_to_dict

from app.database.models.account_owner import AccountOwnerEntity
from app.database.provider import BaseModel

from app.config.enums.account import AccountStates

from app.interfaces.account import AccountInterface


class AccountEntity(BaseModel):
    account_id = AutoField(primary_key=True)
    agency = CharField(max_length=10, default="0001")
    checking_account_number = IntegerField()
    state = CharField(default=AccountStates.ACTIVE.value)
    balance = DecimalField(default=0.0)
    daily_limit = DecimalField(default=2000.0)
    account_owner = ForeignKeyField(AccountOwnerEntity, backref="accounts")
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(null=True)
    closed_at = DateTimeField(null=True)

    class Meta:
        table_name = "account"

    def to_interface(self):
        fields = model_to_dict(self)
        return AccountInterface(**fields)
