from datetime import date, datetime, timedelta
from typing import List
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
        try:
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
        except Exception as e:
            raise e

    @db.atomic()
    async def get_transactions_by_period(
        self, account_id: int, start_date: date, end_date: date
    ) -> List[TransactionEntity]:
        try:
            query = (TransactionEntity
                    .select()
                    .where(
                        (TransactionEntity.account == account_id) &
                        (fn.DATE(TransactionEntity.created_at) >= start_date) &
                        (fn.DATE(TransactionEntity.created_at) <= end_date)
                    )
                    .order_by(TransactionEntity.created_at.desc()))
            return list(query)
        except Exception as e:
            raise e
