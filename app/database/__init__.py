from app.database.models.account import AccountEntity

from app.database.models.account_owner import AccountOwnerEntity
from app.database.provider import DataBaseProvider

models = [
    AccountOwnerEntity,
    AccountEntity,
]

provider = DataBaseProvider.get_provider()
db = provider
db.connect()
db.create_tables(models=[*models])
