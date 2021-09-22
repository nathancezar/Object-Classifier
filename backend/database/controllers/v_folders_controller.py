from database.models import v_folders_model
from database import connection


class vFoldersController():
    def __init__(self):
        connection.database.connect(reuse_if_open=True)

    def get(self):
        try:
            folders = v_folders_model.getAll()
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
                    "processed_count": folder.total_processed,
                    "post_processed_count": folder.total_post_processed,
                    "total_count": folder.total_images,
                }
                if folder.user_id is not None:
                    data["user"] = folder.user.name
                foldersList.append(data)
            return foldersList
        except Exception as ex:
            raise ex
