from database.models import items_model
from database import connection


class ItemsController():
    def __init__(self):
        connection.database.connect(reuse_if_open=True)

    def get(self):
        try:
            items = items_model.getAll()
            if len(items) == 0:
                return ""

            itemsList = []
            for item in items:
                itemsList.append({
                    "id": item.id,
                    "description": item.description,
                    "color": item.color,
                    "visible": item.visible,
                })
            return itemsList
        except Exception as ex:
            raise ex
