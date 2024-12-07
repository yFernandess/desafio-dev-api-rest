from peewee import DoesNotExist

from app.config.exceptions.general import ObjectNotFound
from app.database import db
from app.database.models.account_owner import AccountOwnerEntity
from app.interfaces.account_owner import AccountOwnerInterface


class AccountOwnerRepository:
    def __init__(self):
        pass

    @db.atomic()
    async def create_account_owner(self, account_owner: AccountOwnerInterface) -> AccountOwnerInterface:
        try:
            fields = account_owner.dict()
            account_owner_entity = AccountOwnerEntity.create(**fields)

            return account_owner_entity.to_interface()
        except Exception as e:
            raise e

    @db.atomic()
    async def get_account_owner_by_id(self, id: int) -> AccountOwnerInterface:
        try:
            query = AccountOwnerEntity.get(AccountOwnerEntity.id == id)
            return query.to_interface()
        except DoesNotExist:
            raise ObjectNotFound(
                object_name="account_owner_entity",
            )

    @db.atomic()
    async def delete_account_owner(self, cpf: str):
        try:
            query = AccountOwnerEntity.delete().where(AccountOwnerEntity.cpf == cpf)
            query.execute()
        except Exception as e:
          raise e
