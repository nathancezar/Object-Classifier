from peewee import CharField, BooleanField
from database import connection


class UsersModel(connection.BaseModel):
    name = CharField(max_length=50)
    login = CharField(max_length=10)
    password = CharField(max_length=100)
    privileged = BooleanField(default=False)

    class Meta:
        table_name = "users"

def getByLogin(login):
    try:
        return UsersModel.select().where(UsersModel.login == login).get()
    except UsersModel.DoesNotExist:
        return None
    except Exception as ex:
        raise ex
