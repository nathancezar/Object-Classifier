import datetime
from peewee import CharField, ForeignKeyField, BooleanField, DateTimeField
from database import connection
from database.models.folders_model import FoldersModel

class ImagesModel(connection.BaseModel):
    name = CharField(max_length=50)
    path = CharField(max_length=150)
    folder = ForeignKeyField(column_name="folder_id", field="id", model=FoldersModel)
    processed = BooleanField(default=False)
    post_processed = BooleanField(default=False)
    last_processed = DateTimeField(null=True)

    class Meta:
        table_name = "images"

def getById(imageId):
    try:
        return ImagesModel.select().where(ImagesModel.id == imageId).get()
    except ImagesModel.DoesNotExist:
        return None
    except Exception as ex:
        raise ex

def getNextByFolderId(folderId):
    try:    
        return (ImagesModel
                .select()
                .where(ImagesModel.folder==folderId)
                .where(ImagesModel.processed==False)
                .order_by(ImagesModel.name.asc())
                .get())
    except ImagesModel.DoesNotExist:
        return None
    except Exception as ex:
        raise ex

def getPreviousByFolderId(folderId):
    try:    
        return (ImagesModel
                .select()
                .where(ImagesModel.folder==folderId)
                .where(ImagesModel.processed==True)
                .order_by(ImagesModel.name.desc())
                .get())
    except ImagesModel.DoesNotExist:
        return None
    except Exception as ex:
        raise ex

def getNextForPostProcessing(folderId):
    try:
        return (ImagesModel
                .select()
                .where(ImagesModel.folder==folderId)
                .where(ImagesModel.post_processed==False)
                .order_by(ImagesModel.name.asc())
                .get())
    except ImagesModel.DoesNotExist:
        return None
    except Exception as ex:
        raise ex

def getPreviousForPostProcessing(folderId):
    try:
        return (ImagesModel
                .select()
                .where(ImagesModel.folder==folderId)
                .where(ImagesModel.post_processed==True)
                .order_by(ImagesModel.name.desc())
                .get())
    except ImagesModel.DoesNotExist:
        return None
    except Exception as ex:
        raise ex

def updateProcessed(imageId, value):
    try:
        return (ImagesModel
                .update(processed=value, last_processed=datetime.datetime.now())
                .where(ImagesModel.id==imageId)
                .execute())
    except ImagesModel.DoesNotExist:
        return None
    except Exception as ex:
        raise ex

def updatePostProcessed(imageId, value):
    try:
        return (ImagesModel
                .update(post_processed=value)
                .where(ImagesModel.id==imageId)
                .execute())
    except ImagesModel.DoesNotExist:
        return None
    except Exception as ex:
        raise ex

def clearAllPostProcessed(folderId):
    try:
        return (ImagesModel
                .update(post_processed=False)
                .where(ImagesModel.folder==folderId)
                .execute())
    except ImagesModel.DoesNotExist:
        return None
    except Exception as ex:
        raise ex

def insertMany(images):
    try:
        fields = [
            ImagesModel.name, ImagesModel.path,
            ImagesModel.folder, ImagesModel.processed
        ]
        ImagesModel.insert_many(images, fields=fields).execute()
    except Exception as ex:
        raise ex

def getAllByFolderId(folderId, processed=False):
    try:
        return (ImagesModel
                .select()
                .where(ImagesModel.folder==folderId)
                .where(ImagesModel.processed==processed)
                .order_by(ImagesModel.name))
    except ImagesModel.DoesNotExist:
        return None
    except Exception as ex:
        raise ex
