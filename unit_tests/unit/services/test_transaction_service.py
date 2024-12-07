import pytest
from unittest.mock import AsyncMock, patch
from playhouse.shortcuts import model_to_dict

from app.config.enums.account import AccountStates
from app.config.enums.transaction import TransactionType
from app.database.models.transaction import TransactionEntity
from app.interfaces.account import AccountInterface
from app.services.transaction_service import TransactionService
from app.interfaces.transaction import RequestDepositInterface, RequestWithdrawInterface, TransactionInterface, RequestStatementInterface
from datetime import datetime

@pytest.fixture
def transaction_service():
    with patch('app.services.transaction_service.TransactionRepository') as MockTransactionRepository:
        transaction_repository = MockTransactionRepository.return_value
        service = TransactionService()
        service._transaction_repository = transaction_repository
        yield service

@pytest.mark.asyncio
async def test_get_statement_by_period(transaction_service):
    # Scenario
    payload = RequestStatementInterface(
        account_id=1,
        start_date=datetime(2023, 1, 1),
        end_date=datetime(2023, 12, 31)
    )
    transactions = [
        TransactionEntity(
            transaction_id=1,
            account=1,
            amount=100.0,
            transaction_type=TransactionType.DEPOSIT,
            created_at=datetime(2023, 1, 10)
        ),
        TransactionEntity(
            transaction_id=2,
            account=1,
            amount=-50.0,
            transaction_type=TransactionType.WITHDRAW,
            created_at=datetime(2023, 1, 15)
        )
    ]

    transaction_service._transaction_repository.get_transactions_by_period = AsyncMock(return_value=transactions)
    
    # Action
    result = await transaction_service.get_statement_by_period(payload)
    
    # Result
    expected_result = [TransactionInterface(**model_to_dict(transaction)) for transaction in transactions]
    assert result == expected_result
    transaction_service._transaction_repository.get_transactions_by_period.assert_called_once_with(
        account_id=payload.account_id,
        start_date=payload.start_date,
        end_date=payload.end_date
    )


@pytest.mark.asyncio
async def test_get_statement_by_period_exception(transaction_service):
    payload = RequestStatementInterface(
        account_id=1,
        start_date=datetime(2023, 1, 1),
        end_date=datetime(2023, 12, 31)
    )

    transaction_service._transaction_repository.get_transactions_by_period = AsyncMock(side_effect=Exception("Error"))

    with pytest.raises(Exception, match="Error"):
        await transaction_service.get_statement_by_period(payload)

    transaction_service._transaction_repository.get_transactions_by_period.assert_called_once_with(
        account_id=payload.account_id,
        start_date=payload.start_date,
        end_date=payload.end_date
    )


@pytest.mark.asyncio
async def test_deposit(transaction_service):
    # Scenario
    payload = RequestDepositInterface(account_id=1, amount=100.0)
    account = AccountInterface(
        account_id=1,
        account_owner=1,
        agency="0001",
        checking_account_number=12345,
        state=AccountStates.ACTIVE.value,
        balance=0.0,
        daily_limit=2000.0
    )
    updated_account = AccountInterface(
        account_id=1,
        account_owner=1,
        agency="0001",
        checking_account_number=12345,
        state=AccountStates.ACTIVE.value,
        balance=100.0,
        daily_limit=2000.0
    )
    transaction = TransactionInterface(
        transaction_id=1,
        account=1,
        amount=100.0,
        transaction_type=TransactionType.DEPOSIT.value,
        created_at=datetime.now()
    )

    transaction_service._account_repository.get_account_by_id = AsyncMock(return_value=account)
    transaction_service._account_repository.update_account = AsyncMock(return_value=None)
    transaction_service._transaction_repository.create_transaction = AsyncMock(return_value=transaction)
    
    # Action
    result = await transaction_service.deposit(payload)
    
    # Result
    assert result.amount == payload.amount
    assert result.transaction_type == TransactionType.DEPOSIT.value
    transaction_service._account_repository.get_account_by_id.assert_called_once_with(payload.account_id)
    transaction_service._account_repository.update_account.assert_called_once()


@pytest.mark.asyncio
async def test_withdraw(transaction_service):
    # Scenario
    payload = RequestWithdrawInterface(account_id=1, amount=100.0)
    account = AccountInterface(
        account_id=1,
        account_owner=1,
        agency="0001",
        checking_account_number=12345,
        state=AccountStates.ACTIVE.value,
        balance=200.0,
        daily_limit=2000.0
    )
    updated_account = AccountInterface(
        account_id=1,
        account_owner=1,
        agency="0001",
        checking_account_number=12345,
        state=AccountStates.ACTIVE.value,
        balance=100.0,
        daily_limit=2000.0
    )
    transaction = TransactionInterface(
        transaction_id=1,
        account=1,
        amount=-100.0,
        transaction_type=TransactionType.WITHDRAW.value,
        created_at=datetime.now()
    )

    transaction_service._account_repository.get_account_by_id = AsyncMock(return_value=account)
    transaction_service._account_repository.update_account = AsyncMock(return_value=None)
    transaction_service._transaction_repository.get_total_withdrawals = AsyncMock(return_value=0.0)
    transaction_service._transaction_repository.create_transaction = AsyncMock(return_value=transaction)
    
    # Action
    result = await transaction_service.withdraw(payload)
    
    # Result
    assert result.amount == -payload.amount
    assert result.transaction_type == TransactionType.WITHDRAW.value
    transaction_service._account_repository.get_account_by_id.assert_called_once_with(payload.account_id)
    transaction_service._account_repository.update_account.assert_called_once()
    transaction_service._transaction_repository.get_total_withdrawals.assert_called_once_with(
        payload.account_id, datetime.now().date()
    )
