import pytest
from unittest.mock import AsyncMock, patch
from app.config.enums.account import AccountStates
from app.config.exceptions.general import ObjectNotFound
from app.interfaces.account import AccountInterface, RequestBlockAccountInterface, RequestCloseAccountInterface, RequestCreateAccountInterface, RequestUnblockAccountInterface
from app.services.account_service import AccountService
from app.interfaces.account_owner import RequestCreateAccountOwnerInterface, AccountOwnerInterface, RequestRemoveAccountOwnerInterface

@pytest.fixture
def account_service():
    with patch('app.services.account_service.AccountRepository') as MockAccountRepository:
        with patch('app.services.account_service.AccountOwnerRepository') as MockAccountOwnerRepository:
            account_repository = MockAccountRepository.return_value
            account_owner_repository = MockAccountOwnerRepository.return_value
            service = AccountService()
            service.account_repository = account_repository
            service.account_owner_repository = account_owner_repository
            yield service

@pytest.mark.asyncio
async def test_create_owner(account_service):
    # Scenario
    payload = RequestCreateAccountOwnerInterface(name="Yuri Fernandes", cpf="39410675839")
    expected_owner = AccountOwnerInterface(id=1, name="Yuri Fernandes", cpf="39410675839")

    account_service.account_owner_repository.create_account_owner = AsyncMock(return_value=expected_owner)

    # Action
    result = await account_service.create_owner(payload)

    # Result
    assert result == expected_owner


@pytest.mark.asyncio
async def test_remove_owner(account_service):
    # Scenario
    payload = RequestRemoveAccountOwnerInterface(cpf="39410675839")

    account_service.account_owner_repository.delete_account_owner = AsyncMock(return_value=None)
    # Action
    await account_service.remove_owner(payload)
    # Result
    account_service.account_owner_repository.delete_account_owner.assert_called_once_with(payload.cpf)


@pytest.mark.asyncio
async def test_remove_owner_exception(account_service):
    # Scenario
    payload = RequestRemoveAccountOwnerInterface(cpf="39410675839")

    account_service.account_owner_repository.delete_account_owner = AsyncMock(side_effect=Exception("Error"))
    # Action
    with pytest.raises(Exception, match="Error"):
        await account_service.remove_owner(payload)
    # Result
    account_service.account_owner_repository.delete_account_owner.assert_called_once_with(payload.cpf)


@pytest.mark.asyncio
async def test_create_account(account_service):
    # Scenario
    payload = RequestCreateAccountInterface(account_owner_id=1, agency="0001", checking_account_number=12345)
    account_owner = AccountOwnerInterface(id=1, name="Yuri Fernandes", cpf="39410675839")
    expected_account = AccountInterface(
        account_id=1,
        account_owner=1,
        agency="0001",
        checking_account_number=12345,
        state="ACTIVE",
        balance=0.0,
        daily_limit=2000.0
    )

    account_service.account_owner_repository.get_account_owner_by_id = AsyncMock(return_value=account_owner)
    account_service.account_repository.create_account = AsyncMock(return_value=expected_account)
    # Action
    result = await account_service.create_account(payload)
    # Result
    assert result == expected_account
    account_service.account_owner_repository.get_account_owner_by_id.assert_called_once_with(payload.account_owner_id)
    account_service.account_repository.create_account.assert_called_once()


@pytest.mark.asyncio
async def test_create_account_owner_not_found(account_service):
    # Scenario
    payload = RequestCreateAccountInterface(account_owner_id=1, agency="0001", checking_account_number=12345)

    account_service.account_owner_repository.get_account_owner_by_id = AsyncMock(
        side_effect=ObjectNotFound("Account owner not found")
    )
    # Action
    with pytest.raises(ObjectNotFound, match="Account owner not found"):
        await account_service.create_account(payload)
    # Result
    account_service.account_owner_repository.get_account_owner_by_id.assert_called_once_with(payload.account_owner_id)
    account_service.account_repository.create_account.assert_not_called()


@pytest.mark.asyncio
async def test_get_account(account_service):
    # Scenario
    account_id = 1
    expected_account = AccountInterface(
        account_id=1,
        account_owner=1,
        agency="0001",
        checking_account_number=12345,
        state="ACTIVE",
        balance=0.0,
        daily_limit=2000.0
    )

    account_service.account_repository.get_account_by_id = AsyncMock(return_value=expected_account)
    # Action
    result = await account_service.get_account(account_id)
    # Result
    assert result == expected_account
    account_service.account_repository.get_account_by_id.assert_called_once_with(account_id)


@pytest.mark.asyncio
async def test_block_account(account_service):
    # Scenario
    payload = RequestBlockAccountInterface(account_id=1)
    account = AccountInterface(
        account_id=1,
        account_owner=1,
        agency="0001",
        checking_account_number=12345,
        state=AccountStates.ACTIVE.value,
        balance=0.0,
        daily_limit=2000.0
    )
    blocked_account = AccountInterface(
        account_id=1,
        account_owner=1,
        agency="0001",
        checking_account_number=12345,
        state=AccountStates.BLOCKED.value,
        balance=0.0,
        daily_limit=2000.0
    )

    account_service.account_repository.get_account_by_id = AsyncMock(return_value=account)
    account_service.account_repository.block_account = AsyncMock(return_value=blocked_account)
    
    # Action
    result = await account_service.block_account(payload)
    
    # Result
    assert result.state == AccountStates.BLOCKED.value
    account_service.account_repository.get_account_by_id.assert_called_once_with(payload.account_id)
    account_service.account_repository.block_account.assert_called_once()


@pytest.mark.asyncio
async def test_unblock_account(account_service):
    # Scenario
    payload = RequestUnblockAccountInterface(account_id=1)
    blocked_account = AccountInterface(
        account_id=1,
        account_owner=1,
        agency="0001",
        checking_account_number=12345,
        state=AccountStates.BLOCKED.value,
        balance=0.0,
        daily_limit=2000.0
    )
    unblocked_account = AccountInterface(
        account_id=1,
        account_owner=1,
        agency="0001",
        checking_account_number=12345,
        state=AccountStates.ACTIVE.value,
        balance=0.0,
        daily_limit=2000.0
    )

    account_service.account_repository.get_account_by_id = AsyncMock(return_value=blocked_account)
    account_service.account_repository.unblock_account = AsyncMock(return_value=unblocked_account)
    
    # Action
    result = await account_service.unblock_account(payload)
    
    # Result
    assert result.state == AccountStates.ACTIVE.value
    account_service.account_repository.get_account_by_id.assert_called_once_with(payload.account_id)
    account_service.account_repository.unblock_account.assert_called_once()


@pytest.mark.asyncio
async def test_close_account(account_service):
    # Scenario
    payload = RequestCloseAccountInterface(account_id=1)
    account = AccountInterface(
        account_id=1,
        account_owner=1,
        agency="0001",
        checking_account_number=12345,
        state=AccountStates.ACTIVE.value,
        balance=0.0,
        daily_limit=2000.0
    )
    closed_account = AccountInterface(
        account_id=1,
        account_owner=1,
        agency="0001",
        checking_account_number=12345,
        state=AccountStates.CLOSED.value,
        balance=0.0,
        daily_limit=2000.0
    )

    account_service.account_repository.get_account_by_id = AsyncMock(return_value=account)
    account_service.account_repository.close_account = AsyncMock(return_value=closed_account)
    
    # Action
    result = await account_service.close_account(payload)
    
    # Result
    assert result.state == AccountStates.CLOSED.value
    account_service.account_repository.get_account_by_id.assert_called_once_with(payload.account_id)
    account_service.account_repository.close_account.assert_called_once()
