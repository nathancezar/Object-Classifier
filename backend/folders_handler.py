import json
import traceback
import get_dataset_labels
import insert_database
from base_handler import BaseHandler
from database.controllers.folders_controller import FoldersController


class FoldersHandler(BaseHandler):
    def get(self):
        try:
            foldersController = FoldersController()
            folders = foldersController.get()
            self.set_status(200)
            self.write({"folders": folders})
        except Exception as ex:
            traceback.print_exc()
            print(ex)
            self.set_status(500)

    def post(self):
        try:
            newFolder = json.loads(self.request.body)
            foldersController = FoldersController()
            folderId = foldersController.insert(newFolder)
            if folderId:
                self.set_status(200)
            else:
                self.set_status(500)
        except Exception as ex:
            traceback.print_exc()
            print(ex)
            self.set_status(500)

    def put(self):
        if "/processed" in self.request.uri:
            self.updateProcessed()
        elif "/user_id" in self.request.uri:
            self.checkAndUpdateUserId()
        elif "/export_folder" in self.request.uri:
            self.exportFolder()
        elif "/export_all" in self.request.uri:
            self.exportAll()
        elif "/export_by_type" in self.request.uri:
            self.exportByType()
        elif "/insert_database" in self.request.uri:
            self.insertDatabase()
        elif "/flag" in self.request.uri:
            self.flagFolder()
        elif "/unflag" in self.request.uri:
            self.unflagFolder()
        elif "/deleted" in self.request.uri:
            self.updateDeleted()

    def insertDatabase(self):
        try:
            insert_database.insertDatabase({"path": "/home/nathancezar/Documentos/yoco/items"})
            self.set_status(200)
        except Exception as ex:
            traceback.print_exc()
            print(ex)
            self.set_status(500)

    def exportFolder(self):
        try:
            request = json.loads(self.request.body)
            foldersController = FoldersController()
            folder = foldersController.getById(request["folder_id"])
            request["folder"] = folder
            request["images_out"] = "/mnt/yoco_datasets/images"
            request["labels_out"] = "/mnt/yoco_datasets/labels"
            request["tar_out"] = "/mnt/yoco_datasets"

            get_dataset_labels.exportFolder(request)
            foldersController.updateExported({
                "folder_id": folder["id"],
                "exported": True,
            })
            self.write(folder)
            self.set_status(200)
        except Exception as ex:
            traceback.print_exc()
            print(ex)
            self.set_status(500)

    def exportAll(self):
        try:
            request = json.loads(self.request.body)
            foldersController = FoldersController()
            folders = foldersController.getAllUnexported()
            request["folders"] = folders
            request["images_out"] = "/mnt/yoco_datasets/images"
            request["labels_out"] = "/mnt/yoco_datasets/labels"
            request["tar_out"] = "/mnt/yoco_datasets"

            get_dataset_labels.exportAll(request)
            for folder in folders:
                foldersController.updateExported({
                    "folder_id": folder["id"],
                    "exported": True,
                })
            self.set_status(200)
        except Exception as ex:
            traceback.print_exc()
            print(ex)
            self.set_status(500)

    def exportByType(self):
        try:
            request = json.loads(self.request.body)
            request["images_out"] = "/mnt/test_datasets/images"
            request["labels_out"] = "/mnt/test_datasets/labels"
            request["tar_out"] = "/mnt/test_datasets"
            get_dataset_labels.exportByType(request)
            self.set_status(200)
        except Exception as ex:
            traceback.print_exc()
            print(ex)
            self.set_status(500)

    def updateProcessed(self):
        try:
            folder = json.loads(self.request.body)
            foldersController = FoldersController()
            foldersController.updateProcessed(folder)
            self.set_status(200)
        except Exception as ex:
            traceback.print_exc()
            print(ex)
            self.set_status(500)

    def checkAndUpdateUserId(self):
        try:
            request = json.loads(self.request.body)
            foldersController = FoldersController()
            folder = foldersController.getById(request["folder_id"])
            response = True
            if folder["user_id"] is None:
                foldersController.updateUserId(request)
            elif folder["user_id"] != request["user_id"]:
                response = False
            self.write({"response" : response})
            self.set_status(200)
        except Exception as ex:
            traceback.print_exc()
            print(ex)
            self.set_status(500)

    def flagFolder(self):
        try:
            request = json.loads(self.request.body)
            foldersController = FoldersController()
            foldersController.flagFolder(request)
            self.set_status(200)
        except Exception as ex:
            traceback.print_exc()
            print(ex)
            self.set_status(500)

    def unflagFolder(self):
        try:
            request = json.loads(self.request.body)
            foldersController = FoldersController()
            foldersController.unflagFolder(request)
            self.set_status(200)
        except Exception as ex:
            traceback.print_exc()
            print(ex)
            self.set_status(500)

    def updateDeleted(self):
        try:
            folder = json.loads(self.request.body)
            foldersController = FoldersController()
            foldersController.updateDeleted(folder)
            self.write(folder)
            self.set_status(200)
        except Exception as ex:
            traceback.print_exc()
            print(ex)
            self.set_status(500)
