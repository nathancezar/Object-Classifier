from peewee import FloatField, ForeignKeyField
from database import connection
from database.models.items_model import ItemsModel
from database.models.images_model import ImagesModel

class LabelsModel(connection.BaseModel):
    image = ForeignKeyField(column_name="image_id", field="id", model=ImagesModel)
    x_center = FloatField()
    y_center = FloatField()
    width = FloatField()
    height = FloatField()
    item = ForeignKeyField(column_name="item_id", field="id", model=ItemsModel)

    class Meta:
        table_name = "labels"

def insert(label, imageId):
    try:
        return (LabelsModel
                .insert(image=imageId, item=label["item_id"], x_center=float(label["x_center"]),
                        y_center=float(label["y_center"]), width=float(label["width"]),
                        height=float(label["height"])).execute())
    except Exception as ex:
        raise ex

def getAllByImageId(imageId):
    try:
        return(LabelsModel
               .select()
               .where(LabelsModel.image==imageId))
    except LabelsModel.DoesNotExists:
        return None
    except Exception as ex:
        raise ex

def deleteByImageId(imageId):
    try:
        LabelsModel.delete().where(LabelsModel.image == imageId).execute()
    except Exception as ex:
        raise ex

def getAllByItemId(itemId):
    try:
        return(LabelsModel
               .select()
               .where(LabelsModel.item==itemId))
    except LabelsModel.DoesNotExists:
        return None
    except Exception as ex:
        raise ex
