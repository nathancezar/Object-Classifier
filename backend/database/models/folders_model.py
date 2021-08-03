from peewee import CharField, BooleanField, ForeignKeyField
from database import connection
from database.models.users_model import UsersModel


class FoldersModel(connection.BaseModel):
    name = CharField(max_length=50)
    path = CharField(max_length=100)
    user = ForeignKeyField(column_name="user_id", field="id", model=UsersModel)
    processed = BooleanField(default=False)
    exported = BooleanField(default=False)
    verified = BooleanField(default=False)
    flagged = BooleanField(default=False)
    flag_description = CharField(max_length=300)
    deleted = BooleanField(default=False)

    class Meta:
        table_name = "folders"

def getAll():
    try:
        return FoldersModel.select().order_by(FoldersModel.name)
    except FoldersModel.DoesNotExists:
        return None
    except Exception as ex:
        raise ex

def getByName(name):
    try:
        return FoldersModel.select().where(FoldersModel.name == name).get()
    except FoldersModel.DoesNotExist:
        return None
    except Exception as ex:
        raise ex

def getAllUnexported():
    try:
        return (FoldersModel
                .select()
                .where(FoldersModel.processed==True)
                .where(FoldersModel.flagged==False)
                .where(FoldersModel.deleted==False)
                .where(FoldersModel.exported==False))
    except FoldersModel.DoesNotExist:
        return None
    except Exception as ex:
        raise ex

def insert(folder):
    try:
        return (FoldersModel
                .insert(name=folder["name"], path=folder["path"],
                        user=folder["user_id"]).execute())
    except Exception as ex:
        raise ex

def getFolderById(folderId):
    try:
        return FoldersModel.select().where(FoldersModel.id == folderId).get()
    except FoldersModel.DoesNotExist:
        return None
    except Exception as ex:
        raise ex

def updateProcessed(folder):
    try:
        (FoldersModel
            .update(processed=folder["processed"])
            .where(FoldersModel.id==folder["folder_id"])
            .execute()
        )
    except Exception as ex:
        raise ex

def updateUserId(folder):
    try:
        (FoldersModel
            .update(user=folder["user_id"])
            .where(FoldersModel.id==folder["folder_id"])
            .execute()
        )
    except Exception as ex:
        raise ex

def updateExported(folder):
    try:
        (FoldersModel
            .update(exported=folder["exported"])
            .where(FoldersModel.id==folder["folder_id"])
            .execute()
        )
    except Exception as ex:
        raise ex

def updateVerified(folder):
    try:
        (FoldersModel
            .update(verified=folder["verified"])
            .where(FoldersModel.id==folder["folder_id"])
            .execute()
        )
    except Exception as ex:
        raise ex

def flagFolder(folder):
    try:
        (FoldersModel
            .update(flagged=True, flag_description=folder['flag_description'])
            .where(FoldersModel.id==folder["folder_id"])
            .execute()
        )
    except Exception as ex:
        raise ex

def unflagFolder(folder):
    try:
        (FoldersModel
            .update(flagged=False, flag_description='')
            .where(FoldersModel.id==folder["folder_id"])
            .execute()
        )
    except Exception as ex:
        raise ex

def updateDeleted(folder):
    try:
        (FoldersModel
            .update(deleted=folder["deleted"])
            .where(FoldersModel.id==folder["folder_id"])
            .execute()
        )
    except Exception as ex:
        raise ex