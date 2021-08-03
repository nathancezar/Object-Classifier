import json
import traceback
import base64
from base_handler import BaseHandler
from database.controllers.folders_controller import FoldersController
from database.controllers.images_controller import ImagesController
from database.controllers.items_controller import ItemsController
from database.controllers.labels_controller import LabelsController


class ImagesHandler(BaseHandler):
    def get(self):
        if "/images/next" in self.request.uri:
            self.getNextImage()
        elif "/images/previous" in self.request.uri:
            self.getPreviousImage()
        elif "/items" in self.request.uri:
            self.getItems()

    def readLabelsAndData(self, image):
        labelsController = LabelsController()
        image["labels"] = labelsController.getAllByImageId(image["id"])
        with open(image["path"], "rb") as f:
            image["data"] = base64.b64encode(f.read()).decode('utf-8')

    def getNextImage(self):
        try:
            folderId = self.get_argument("folder_id", None)
            postProcessing = bool(int(self.get_argument("post_processing", None)))
            imagesController = ImagesController()
            image = imagesController.getByFolderId(folderId, postProcessing=postProcessing)
            if image:
                self.readLabelsAndData(image)
                self.write(image)
            self.set_status(200)
        except Exception as ex:
            traceback.print_exc()
            print(ex)
            self.set_status(500)

    def getPreviousImage(self):
        try:
            currentImageId = self.get_argument("image_id", None)
            folderId = self.get_argument("folder_id", None)
            postProcessing = bool(int(self.get_argument("post_processing", None)))
            imagesController = ImagesController()
            if postProcessing:
                imagesController.updatePostProcessed(currentImageId, value=False)
            else:
                imagesController.updateProcessed(currentImageId, value=False)
            image = imagesController.getByFolderId(folderId,
                ascending=False, postProcessing=postProcessing)
            if image:
                self.readLabelsAndData(image)
                self.write(image)
            self.set_status(200)
        except Exception as ex:
            traceback.print_exc()
            print(ex)
            self.set_status(500)

    def getItems(self):
        try:
            itemsController = ItemsController()
            items = itemsController.get()
            self.write({"items": items})
            self.set_status(200)
        except Exception as ex:
            traceback.print_exc()
            print(ex)
            self.set_status(500)

    def post(self):
        try:
            request = json.loads(self.request.body)
            labelsController = LabelsController()
            imagesController = ImagesController()
            imageId = request["image_id"]
            labelsController.deleteByImageId(imageId)
            for label in request["labels"]:
                labelsController.insert(label, imageId)
            imagesController.updateProcessed(imageId, value=True)
            self.set_status(200)
        except Exception as ex:
            traceback.print_exc()
            print(ex)
            self.set_status(500)

    def put(self):
        if "/clear" in self.request.uri:
            self.clearPostProcessed()
        elif "/post_processed" in self.request.uri:
            self.updatePostProcessed()

    def clearPostProcessed(self):
        try:
            request = json.loads(self.request.body)
            imagesController = ImagesController()
            imagesController.clearAllPostProcessed(request["folder_id"])
            foldersController = FoldersController()
            foldersController.updateVerified(request)
            self.set_status(200)
        except Exception as ex:
            traceback.print_exc()
            print(ex)
            self.set_status(500)

    def updatePostProcessed(self):
        try:
            request = json.loads(self.request.body)
            imagesController = ImagesController()
            imagesController.updatePostProcessed(request["image_id"], value=True)
            self.set_status(200)
        except Exception as ex:
            traceback.print_exc()
            print(ex)
            self.set_status(500)
