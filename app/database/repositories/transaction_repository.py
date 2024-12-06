from datetime import datetime, timedelta
from peewee import fn

from app.config.enums.transaction import TransactionType
from app.database import db
from app.database.models.transaction import TransactionEntity
from app.interfaces.transaction import TransactionInterface


class TransactionRepository():

    @db.atomic()
    async def create_transaction(self, transaction: TransactionInterface) -> TransactionInterface:
        try:
            fields = transaction.dict()
            transaction_entity = TransactionEntity.create(**fields)

            return transaction_entity.to_interface()
        except Exception as e:
            raise e

    @db.atomic()
    async def get_total_withdrawals(self, account_id: int, date: datetime.date):
        total_withdrawals = (TransactionEntity
                             .select(fn.SUM(TransactionEntity.amount))
                             .where(
                                 (TransactionEntity.account == account_id) &
                                 (TransactionEntity.transaction_type == TransactionType.WITHDRAW.value) &
                                 (TransactionEntity.created_at >= date) &
                                 (TransactionEntity.created_at < date + timedelta(days=1))
                             )
                             .scalar() or 0)
        return total_withdrawals
