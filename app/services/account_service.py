import logging
import random

from app.config.enums.account import AccountStates
from app.config.exceptions.general import ObjectNotFound
from app.database.repositories.account_owner_repository import AccountOwnerRepository
from app.database.repositories.account_repository import AccountRepository
from app.interfaces.account import (
    AccountInterface,
    RequestBlockAccountInterface,
    RequestCloseAccountInterface,
    RequestCreateAccountInterface,
    RequestUnblockAccountInterface
)
from app.interfaces.account_owner import (
    AccountOwnerInterface, RequestCreateAccountOwnerInterface, RequestRemoveAccountOwnerInterface
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()


class AccountService:
    def __init__(
        self,
    ):
        self.account_repository = AccountRepository()
        self.account_owner_repository = AccountOwnerRepository()

    async def create_owner(self, payload: RequestCreateAccountOwnerInterface) -> AccountOwnerInterface:
        try:
            logger.info(f"Creating account owner with cpf: {payload.cpf}")
            account_owner = AccountOwnerInterface(
                name=payload.name,
                cpf=payload.cpf,
            )
            account_owner_inserted = await self.account_owner_repository.create_account_owner(account_owner)
            logger.info(f"Account owner with cpf: {payload.cpf} created")
            return account_owner_inserted
        except Exception as e:
            logger.error(f"Unable to create owner with cpf: {payload.cpf}. Error: {e}")
            raise e

    async def remove_owner(self, payload: RequestRemoveAccountOwnerInterface):
        try:
            logger.info(f"Removing account owner with cpf: {payload.cpf}")

            await self.account_owner_repository.delete_account_owner(payload.cpf)
            logger.info(f"Account owner with cpf: {payload.cpf} removed")
        except Exception as e:
          logger.error(f"Unable to remove owner with cpf: {payload.cpf}. Error: {e}")
          raise e

    async def create_account(self, payload: RequestCreateAccountInterface):
        try:
            logger.info(
                f"Creating account with account_owner: {payload.account_owner_id}"
            )

            try:
                account_owner = await self.account_owner_repository.get_account_owner_by_id(
                    payload.account_owner_id
                )
            except ObjectNotFound as e:
                logger.error(
                    f"Unable to get account owner with account_owner_id: {payload.account_owner_id}. Error: {e}"
                )
                raise e

            checking_account_number = random.sample(range(1, 1000 + 1), 1)
            account = AccountInterface(
                checking_account_number=checking_account_number[0],
                account_owner=account_owner.id,
            )
            account_inserted = await self.account_repository.create_account(account)
            logger.info(f"Account with account_owner: {account_owner.id} created")
            return account_inserted
        except Exception as e:
            logger.error(f"Unable to create account. Error: {e}")
            raise e

    async def get_account(self, account_id: int) -> AccountInterface:
        try:
            logger.info(f"Getting account with account_id: {account_id}")
            account = await self.account_repository.get_account_by_id(account_id)
            logger.info(f"Account with account_id: {account_id} retrieved")
            return account
        except ObjectNotFound as e:
            logger.error(f"Unable to get account with account_id: {account_id}. Error: {e}")
            raise e

    async def block_account(self, payload: RequestBlockAccountInterface) -> AccountInterface:
        try:
            logger.info(f"Blocking account with account_id: {payload.account_id}")
            try:
                account = await self.account_repository.get_account_by_id(payload.account_id)
            except ObjectNotFound as e:
                logger.error(f"Unable to get account with account_id: {payload.account_id}. Error: {e}")
                raise e

            account_updated = await self.account_repository.block_account(
                account_id=account.account_id,
            )
            logger.info(f"Account with account_id: {payload.account_id} blocked")
            return account_updated
        except Exception as e:
            logger.error(f"Unable to block account with account_id: {payload.account_id}. Error: {e}")
            raise e

    async def unblock_account(self, payload: RequestUnblockAccountInterface) -> AccountInterface:
        try:
            logger.info(f"Unblocking account with account_id: {payload.account_id}")

            try:
                account = await self.account_repository.get_account_by_id(payload.account_id)
            except ObjectNotFound as e:
                logger.error(f"Unable to get account with account_id: {payload.account_id}. Error: {e}")
                raise e

            account_updated = await self.account_repository.unblock_account(
                account_id=account.account_id,
            )
            logger.info(f"Account with account_id: {payload.account_id} unblocked")
            return account_updated
        except Exception as e:
            logger.error(f"Unable to unblock account with account_id: {payload.account_id}. Error: {e}")
            raise e

    async def close_account(self, payload: RequestCloseAccountInterface) -> AccountInterface:
        try:
            logger.info(f"Closing account with account_id: {payload.account_id}")

            try:
                account = await self.account_repository.get_account_by_id(payload.account_id)
            except ObjectNotFound as e:
                logger.error(f"Unable to get account with account_id: {payload.account_id}. Error: {e}")
                raise e

            account_updated = await self.account_repository.close_account(
                account_id=account.account_id,
                state=AccountStates.CLOSED.value
            )
            logger.info(f"Account with account_id: {payload.account_id} closed")
            return account_updated
        except Exception as e:
            logger.error(f"Unable to close account with account_id: {payload.account_id}. Error: {e}")
            raise e
