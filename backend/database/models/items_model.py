from peewee import CharField, BooleanField
from database import connection


class ItemsModel(connection.BaseModel):
    description = CharField(max_length=50)
    color = CharField(max_length=6)
    visible = BooleanField(default=True)

    class Meta:
        table_name = "items"

def getAll():
    try:
        return ItemsModel.select()
    except ItemsModel.DoesNotExists:
        return None
    except Exception as ex:
        raise ex
