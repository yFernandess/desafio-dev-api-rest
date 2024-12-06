from datetime import datetime
import logging
from typing import List

from app.config.enums.account import AccountStates
from app.config.enums.transaction import TransactionType
from app.config.exceptions.general import (
    DailyLimitReached, InsufficientBalance, ObjectNotFound, TransactionNotAllowed
)
from app.database.repositories.account_repository import AccountRepository
from app.database.repositories.transaction_repository import TransactionRepository
from app.interfaces.transaction import (
    RequestDepositInterface, RequestStatementInterface, RequestWithdrawInterface, TransactionInterface
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()


class TransactionService:
    def __init__(
        self,
        account_repository: AccountRepository = None,
        transaction_repository: TransactionRepository = None,
    ):
        self._account_repository = account_repository or AccountRepository()
        self._transaction_repository = transaction_repository or TransactionRepository()

    async def get_statement_by_period(self, payload: RequestStatementInterface) -> List[TransactionInterface]:
        try:
            logger.info(f"Getting statement for account: {payload.account_id}")
            transactions = await self._transaction_repository.get_transactions_by_period(
                account_id=payload.account_id,
                start_date=payload.start_date,
                end_date=payload.end_date,
            )
            logger.info(f"Got statement for account: {payload.account_id}")
            return [TransactionInterface(**transaction) for transaction in transactions]
        except Exception as e:
            logger.error(f"Unable to get statement for account: {payload.account_id}. Error: {e}")
            raise e

    async def deposit(self, payload: RequestDepositInterface) -> TransactionInterface:
        try:
            logger.info(f"Depositing {payload.amount} to account: {payload.account_id}")
            try:
                account = await self._account_repository.get_account_by_id(payload.account_id)
            except ObjectNotFound as e:
                logger.error(f"Unable to get account with account_id: {payload.account_id}. Error: {e}")
                raise e

            if account.state != AccountStates.ACTIVE.value:
                raise TransactionNotAllowed()

            account.balance += payload.amount
            account.updated_at = datetime.now()
            await self._account_repository.update_account(account)

            transaction = TransactionInterface(
                account=account.account_id,
                amount=payload.amount,
                transaction_type=TransactionType.DEPOSIT.value,
            )
            transaction_inserted = await self._transaction_repository.create_transaction(transaction)

            logger.info(f"Deposited {payload.amount} to account: {payload.account_id}")
            return transaction_inserted
        except Exception as e:
            logger.error(f"Unable to deposit {payload.amount} to account: {payload.account_id}. Error: {e}")
            raise e

    async def withdraw(self, payload: RequestWithdrawInterface) -> TransactionInterface:
        try:
            try:
                account = await self._account_repository.get_account_by_id(payload.account_id)
            except ObjectNotFound as e:
                logger.error(f"Unable to get account with account_id: {payload.account_id}. Error: {e}")
                raise e

            if account.state != AccountStates.ACTIVE.value:
                raise TransactionNotAllowed()

            if account.balance < payload.amount:
                logger.error(f"Insufficient balance to withdraw {payload.amount} from account: {payload.account_id}")
                raise InsufficientBalance()

            today = datetime.now().date()
            total_withdrawals_today = await self._transaction_repository.get_total_withdrawals(account.account_id, today)
            if total_withdrawals_today + payload.amount > account.daily_limit:
                logger.error(f"Daily limit reached for account: {payload.account_id}")
                raise DailyLimitReached()

            account.balance -= payload.amount
            account.updated_at = datetime.now()
            await self._account_repository.update_account(account)

            transaction = TransactionInterface(
                account=account.account_id,
                amount=payload.amount,
                transaction_type=TransactionType.WITHDRAW.value,
            )
            transaction_inserted = await self._transaction_repository.create_transaction(transaction)

            logger.info(f"Withdrawal {payload.amount} to account: {payload.account_id}")
            return transaction_inserted
        except Exception as e:
            logger.error(f"Unable to withdraw {payload.amount} to account: {payload.account_id}. Error: {e}")
            raise e
