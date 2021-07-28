from database.models import labels_model
from database import connection

class LabelsController():
    def __init__(self):
        connection.database.connect(reuse_if_open=True)

    def insert(self, label, imageId):
        labelId = None
        with connection.database.atomic() as transaction:
            try:
                labelId = labels_model.insert(label, imageId)
            except KeyboardInterrupt:
                transaction.rollback()
                raise ex
            except Exception as ex:
                transaction.rollback()
                raise ex
        return labelId

    def labelObjToDict(self, label):
        try:
            return {
                "id": label.id,
                "image_id": label.image.id,
                "x_center": label.x_center,
                "y_center": label.y_center,
                "width": label.width,
                "height": label.height,
                "item_id": label.item.id
            }
        except Exception as ex:
            raise ex

    def getAllByImageId(self, imageId):
        try:
            labels = labels_model.getAllByImageId(imageId)
            if labels is None:
                return []

            labelsList = []
            for label in labels:
                labelsList.append(self.labelObjToDict(label))
            return labelsList
        except Exception as ex:
            raise ex

    def deleteByImageId(self, imageId):
        try:
            labels_model.deleteByImageId(imageId)
        except Exception as ex:
            raise ex

    def getAllByItemId(self, itemId):
        try:
            labels = labels_model.getAllByItemId(itemId)
            if labels is None:
                return []

            labelsList = []
            for label in labels:
                labelsList.append(self.labelObjToDict(label))
            return labelsList
        except Exception as ex:
            raise ex