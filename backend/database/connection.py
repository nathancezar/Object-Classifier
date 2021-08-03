import os

from peewee import PostgresqlDatabase, Model


_user = os.environ.get("DB_USER")
_password = os.environ.get("DB_PASSWORD")
_host = os.environ.get("DB_HOST")
_port = os.environ.get("DB_PORT")

database = PostgresqlDatabase("db_obj-classify",
                                user=_user,
                                password=_password,
                                host=_host,
                                port=_port)

class BaseModel(Model):
    class Meta:
        database = database