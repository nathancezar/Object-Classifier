from peewee import CharField, IntegerField, BooleanField, ForeignKeyField
from database import connection
from database.models.users_model import UsersModel


class vFoldersModel(connection.BaseModel):
    name = CharField(max_length=50)
    path = CharField(max_length=100)
    user = ForeignKeyField(column_name="user_id", field="id", model=UsersModel)
    processed = BooleanField(default=False)
    exported = BooleanField(default=False)
    verified = BooleanField(default=False)
    flagged = BooleanField(default=False)
    flag_description = CharField(max_length=300)
    deleted = BooleanField(default=False)
    total_images = IntegerField()
    total_processed = IntegerField()
    total_post_processed = IntegerField()

    class Meta:
        table_name = "v_folders"

def getAll():
    try:
        return vFoldersModel.select().order_by(vFoldersModel.name)
    except vFoldersModel.DoesNotExists:
        return None
    except Exception as ex:
        raise ex

def getByFolderId(folderId):
    try:    
        return (vFoldersModel
                .select()
                .where(vFoldersModel.id==folderId)
                .get())
    except vFoldersModel.DoesNotExist:
        return None
    except Exception as ex:
        raise ex

