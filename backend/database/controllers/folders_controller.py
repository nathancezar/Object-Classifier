from database.models import folders_model, images_model
from database import connection


class FoldersController():
    def __init__(self):
        connection.database.connect(reuse_if_open=True)

    def get(self):
        try:
            folders = folders_model.getAll()
            if len(folders) == 0:
                return ""

            foldersList = []
            for folder in folders:
                data = {
                    "id": folder.id,
                    "name": folder.name,
                    "path": folder.path,
                    "user": None,
                    "user_id": folder.user_id,
                    "processed": folder.processed,
                    "exported": folder.exported,
                    "verified": folder.verified,
                    "flagged": folder.flagged,
                    "flag_description": folder.flag_description,
                    "deleted": folder.deleted,
                }
                if folder.user_id is not None:
                    data["user"] = folder.user.name
                foldersList.append(data)
            return foldersList
        except Exception as ex:
            raise ex

    def insert(self, folder):
        folderId = None
        with connection.database.atomic() as transaction:
            try:
                folderId = folders_model.insert(folder)
            except KeyboardInterrupt:
                transaction.rollback()
                raise ex
            except Exception as ex:
                transaction.rollback()
                raise ex
        return folderId

    def updateProcessed(self, folder):
        with connection.database.atomic() as transaction:
            try:
                folders_model.updateProcessed(folder)
            except KeyboardInterrupt:
                transaction.rollback()
                raise ex
            except Exception as ex:
                transaction.rollback()
                raise ex

    def updateUserId(self, folder):
        with connection.database.atomic() as transaction:
            try:
                folders_model.updateUserId(folder)
            except KeyboardInterrupt:
                transaction.rollback()
            except Exception as ex:
                transaction.rollback()
                raise ex

    def updateExported(self, folder):
        with connection.database.atomic() as transaction:
            try:
                folders_model.updateExported(folder)
            except KeyboardInterrupt:
                transaction.rollback()
                raise ex
            except Exception as ex:
                transaction.rollback()
                raise ex

    def updateVerified(self, folder):
        with connection.database.atomic() as transaction:
            try:
                folders_model.updateVerified(folder)
            except KeyboardInterrupt:
                transaction.rollback()
                raise ex
            except Exception as ex:
                transaction.rollback()
                raise ex

    def getByName(self, name):
        try:
            folder = folders_model.getByName(name)
            if not folder:
                return ""
            data = {
                "id": folder.id,
                "name": folder.name,
                "path": folder.path,
                "user": None,
                "user_id": folder.user_id,
                "processed": folder.processed,
                "exported": folder.exported,
                "verified": folder.verified,
                "flagged": folder.flagged,
                "flag_description": folder.flag_description,
                "deleted": folder.deleted,
            }
            if folder.user_id is not None:
                data["user"] = folder.user.name
            return data
        except Exception as ex:
            raise ex

    def getById(self, folderId):
        try:
            folder = folders_model.getFolderById(folderId)
            if not folder:
                return ""
            data = {
                "id": folder.id,
                "name": folder.name,
                "path": folder.path,
                "user": None,
                "user_id": folder.user_id,
                "processed": folder.processed,
                "exported": folder.exported,
                "verified": folder.verified,
                "flagged": folder.flagged,
                "flag_description": folder.flag_description,
                "deleted": folder.deleted,
            }
            if folder.user_id is not None:
                data["user"] = folder.user.name
            return data
        except Exception as ex:
            raise ex

    def getAllUnexported(self):
        try:
            folders = folders_model.getAllUnexported()
            foldersList = []
            for folder in folders:
                data = {
                    "id": folder.id,
                    "name": folder.name,
                    "path": folder.path,
                }
                foldersList.append(data)
            return foldersList
        except Exception as ex:
            raise ex

    def flagFolder(self, folder):
        with connection.database.atomic() as transaction:
            try:
                folders_model.flagFolder(folder)
            except KeyboardInterrupt:
                transaction.rollback()
                raise ex
            except Exception as ex:
                transaction.rollback()
                raise ex

    def unflagFolder(self, folder):
        with connection.database.atomic() as transaction:
            try:
                folders_model.unflagFolder(folder)
            except KeyboardInterrupt:
                transaction.rollback()
                raise ex
            except Exception as ex:
                transaction.rollback()
                raise ex

    def updateDeleted(self, folder):
        with connection.database.atomic() as transaction:
            try:
                folders_model.updateDeleted(folder)
            except KeyboardInterrupt:
                transaction.rollback()
                raise ex
            except Exception as ex:
                transaction.rollback()
                raise ex
