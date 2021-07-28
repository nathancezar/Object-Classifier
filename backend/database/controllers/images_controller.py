from database.models import images_model, folders_model, labels_model, v_folders_model
from database import connection
from peewee import chunked


class ImagesController():
    def __init__(self):
        connection.database.connect(reuse_if_open=True)

    def imageObjToDict(self, image):
        try:
            return {
                "id": image.id,
                "name": image.name,
                "path": image.path,
                "folder_id": image.folder.id,
                "processed": image.processed,
                "post_processed": image.post_processed,
            }
        except Exception as ex:
            raise ex

    def getById(self, imageId):
        image = images_model.getById(imageId)
        if image is None:
            return None
        return self.imageObjToDict(image)

    def getByFolderId(self, folderId, ascending=True, postProcessing=False):
        """
            Pesquisa a próxima imagem (ou anterior) no banco de dados

            @parameters
            - folderId (inteiro): id da pasta

            - ascending (booleano): verdadeiro significa avançar para obter o próximo
            imagem; Falso significa retroceder para obter a imagem anterior

            -postProcessing (Boolean): True significa considerar o campo
            'post_processed' ao selecionar as imagens; Falso significa
            considerando o campo 'processado' durante o SELECT.
        """
        try:
            folder = folders_model.getFolderById(folderId)
            if folder is None:
                return ""

            if postProcessing:
                if ascending:
                    image = images_model.getNextForPostProcessing(folderId)
                else:
                    image = images_model.getPreviousForPostProcessing(folderId)
            else:
                if ascending:
                    image = images_model.getNextByFolderId(folderId)
                else:
                    image = images_model.getPreviousByFolderId(folderId)

            if image is None:
                return ""

            imageDict = self.imageObjToDict(image)
            vFolder = v_folders_model.getByFolderId(folderId)
            imageDict["total_count"] = vFolder.total_images
            imageDict["processed_count"] = vFolder.total_processed
            imageDict["post_processed_count"] = vFolder.total_post_processed
            imageDict["folder_name"] = folder.name
            return imageDict
        except Exception as ex:
            raise ex

    def updateProcessed(self, imageId, value):
        try:
            return images_model.updateProcessed(imageId, value)
        except Exception as ex:
            raise ex

    def updatePostProcessed(self, imageId, value):
        try:
            return images_model.updatePostProcessed(imageId, value)
        except Exception as ex:
            raise ex

    def clearAllPostProcessed(self, folderId):
        try:
            return images_model.clearAllPostProcessed(folderId)
        except Exception as ex:
            raise ex

    def insertMany(self, images):
        with connection.database.atomic() as transaction:
            try:
                for batch in chunked(images, 100):
                    images_model.insertMany(batch)
            except KeyboardInterrupt:
                transaction.rollback()
                raise ex
            except Exception as ex:
                transaction.rollback()
                raise ex

    def getAllByFolderId(self, folderId, processed=False):
        try:
            images = images_model.getAllByFolderId(folderId, processed)
            if images is None:
                return ""

            imagesList = []
            for image in images:
                imagesList.append(self.imageObjToDict(image))
            return imagesList
        except Exception as ex:
            raise ex
