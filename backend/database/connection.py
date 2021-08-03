import os

from peewee import PostgresqlDatabase, Model


user = os.environ.get("DB_USER")
password = os.environ.get("DB_PASSWORD")
host = os.environ.get("DB_HOST")
port = os.environ.get("DB_PORT")

database = PostgresqlDatabase("db_obj-classify", user=user, password=password, host=host, port=port)

class BaseModel(Model):
    class Meta:
        database = database