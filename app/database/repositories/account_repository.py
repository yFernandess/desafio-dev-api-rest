from datetime import datetime
from peewee import DoesNotExist

from app.config.enums.account import AccountStates
from app.config.exceptions.general import ObjectNotFound
from app.database import db
from app.database.models.account import AccountEntity

from app.interfaces.account import AccountInterface


class AccountRepository():
    def __init__(
        self,
    ):
        pass

    @db.atomic()
    async def create_account(self, account: AccountInterface) -> AccountInterface:
        try:
            fields = account.dict()
            account_entity = AccountEntity.create(**fields)

            return account_entity.to_interface()
        except Exception as e:
            raise e

    @db.atomic()
    async def get_account_by_id(self, account_id: int) -> AccountInterface:
        try:
            account_entity = AccountEntity.get(AccountEntity.account_id == account_id)
            return account_entity.to_interface()
        except DoesNotExist:
            raise ObjectNotFound(
                object_name="account_entity",
            )

    @db.atomic()
    async def block_account(self, account_id: int) -> AccountInterface:
        try:
            updated_at = datetime.now()
            query = AccountEntity.update(
                state=AccountStates.BLOCKED.value, updated_at=updated_at
            ).where(AccountEntity.account_id == account_id)
            query.execute()

            account_entity = AccountEntity.get(AccountEntity.account_id == account_id)
            return account_entity.to_interface()
        except Exception as e:
            raise e

    @db.atomic()
    async def unblock_account(self, account_id: int) -> AccountInterface:
        try:
            updated_at = datetime.now()
            query = AccountEntity.update(
                state=AccountStates.ACTIVE.value, updated_at=updated_at
            ).where(AccountEntity.account_id == account_id)
            query.execute()

            account_entity = AccountEntity.get(AccountEntity.account_id == account_id)
            return account_entity.to_interface()
        except Exception as e:
            raise e
    
    @db.atomic()
    async def close_account(self, account_id: int, state: str) -> AccountInterface:
        try:
            updated_at = datetime.now()
            closed_at = datetime.now()
            query = AccountEntity.update(
                state=AccountStates.CLOSED.value, updated_at=updated_at, closed_at=closed_at
            ).where(AccountEntity.account_id == account_id)
            query.execute()

            account_entity = AccountEntity.get(AccountEntity.account_id == account_id)
            return account_entity.to_interface()
        except Exception as e:
            raise e

    @db.atomic()
    async def update_account(self, account: AccountInterface) -> AccountInterface:
        try:
            query = AccountEntity.update(
                agency=account.agency,
                checking_account_number=account.checking_account_number,
                state=account.state,
                balance=account.balance,
                daily_limit=account.daily_limit,
                account_owner=account.account_owner.id,
                updated_at=datetime.now(),
                closed_at=account.closed_at,
            ).where(AccountEntity.account_id == account.account_id)
            query.execute()

            account_entity = AccountEntity.get(AccountEntity.account_id == account.account_id)
            return account_entity.to_interface()
        except Exception as e:
            raise e
