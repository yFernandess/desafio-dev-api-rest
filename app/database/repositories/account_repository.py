from datetime import datetime
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
    async def block_account(self, account_id: int, state: str) -> AccountInterface:
        try:
            updated_at = datetime.now()
            query = AccountEntity.update(
                state=state, updated_at=updated_at
            ).where(AccountEntity.account_id == account_id)
            query.execute()

            account_entity = AccountEntity.get(AccountEntity.account_id == account_id)
            return account_entity.to_interface()
        except Exception as e:
            raise e
