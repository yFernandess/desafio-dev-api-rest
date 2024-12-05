import logging
import random

from app.config.enums.account import AccountStates
from app.database.repositories.account_owner_repository import AccountOwnerRepository
from app.database.repositories.account_repository import AccountRepository
from app.interfaces.account import (
    AccountInterface, RequestBlockAccountInterface, RequestCreateAccountInterface, RequestUnblockAccountInterface
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
            checking_account_number = random.sample(range(1, 1000 + 1), 1)
            account = AccountInterface(
                checking_account_number=checking_account_number[0],
                account_owner=payload.account_owner_id,
            )
            account_inserted = await self.account_repository.create_account(account)
            logger.info(f"Account with account_owner: {payload.account_owner_id} created")
            return account_inserted
        except Exception as e:
            logger.error(f"Unable to create account. Error: {e}")
            raise e

    async def block_account(self, payload: RequestBlockAccountInterface):
        try:
            logger.info(f"Blocking account with account_id: {payload.account_id}")

            account_updated = await self.account_repository.block_account(
                account_id=payload.account_id,
                state=AccountStates.BLOCKED.value,
            )
            logger.info(f"Account with account_id: {payload.account_id} blocked")
            return account_updated
        except Exception as e:
            logger.error(f"Unable to block account with account_id: {payload.account_id}. Error: {e}")

    async def unblock_account(self, payload: RequestUnblockAccountInterface):
        try:
            logger.info(f"Unblocking account with account_id: {payload.account_id}")

            account_updated = await self.account_repository.block_account(
                account_id=payload.account_id,
                state=AccountStates.ACTIVE.value,
            )
            logger.info(f"Account with account_id: {payload.account_id} unblocked")
            return account_updated
        except Exception as e:
            logger.error(f"Unable to unblock account with account_id: {payload.account_id}. Error: {e}")
