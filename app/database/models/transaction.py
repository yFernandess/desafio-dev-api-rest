from datetime import datetime
from peewee import (
    AutoField,
    ForeignKeyField,
    IntegerField,
    DateTimeField,
    DecimalField,
)
from playhouse.shortcuts import model_to_dict

from app.database.models.account import AccountEntity
from app.database.provider import BaseModel
from app.interfaces.transaction import TransactionInterface


class TransactionEntity(BaseModel):
    transaction_id = AutoField(primary_key=True)
    account = ForeignKeyField(AccountEntity, backref="transactions")
    amount = DecimalField()
    transaction_type = IntegerField()  # 'deposit' or 'withdrawal'
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = "transaction"

    def to_interface(self):
        fields = model_to_dict(self)
        return TransactionInterface(**fields)
