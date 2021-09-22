import os

from dotenv import load_dotenv
from peewee import PostgresqlDatabase, Model

load_dotenv()

_database = os.environ.get("DATABASE_URL")
_user = os.environ.get("DB_USER")
_password = os.environ.get("DB_PASSWORD")
_host = os.environ.get("DB_HOST")
_port = os.environ.get("DB_PORT")

database = PostgresqlDatabase(  _database,
                                user=_user,
                                password=_password,
                                host=_host,
                                port=_port)

class BaseModel(Model):
    class Meta:
        database = database