import os

from peewee import DatabaseProxy, Model, SqliteDatabase
# from playhouse.sqlite_ext import SqliteExtDatabase

from app.config.settings import Settings


class DataBaseProvider:
    @staticmethod
    def get_provider():
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'accounts.db')
        return SqliteDatabase(db_path)


class BaseModel(Model):
    class Meta:
        provider = DataBaseProvider.get_provider()
        database = provider
