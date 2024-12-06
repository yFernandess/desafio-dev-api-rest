import os

from peewee import Model, SqliteDatabase


class DataBaseProvider:
    @staticmethod
    def get_provider():
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'accounts.db')
        return SqliteDatabase(db_path)


class BaseModel(Model):
    class Meta:
        provider = DataBaseProvider.get_provider()
        database = provider
