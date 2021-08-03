import os
import argparse
from database.controllers.folders_controller import FoldersController
from database.controllers.images_controller import ImagesController


def insertDatabase(args):
    root = args["path"]
    rootFolders = tuple(map(lambda x: os.path.join(root, x), os.listdir(root)))
    for dirname in rootFolders:
        folders = os.listdir(dirname)

        folderController = FoldersController()
        imageController = ImagesController()

        for f in folders:
            folder = folderController.getByName(f)
            if folder:
                continue
            folderDict = {
                "name": f,
                "path": os.path.join(dirname, f),
                "user_id": None
            }
            fId = folderController.insert(folderDict)

            images = os.listdir(os.path.join(dirname, f))
            images = list(map(lambda img: {"name": img,
                    "path": os.path.join(dirname, f, img),
                    "folder": fId, "processed":False}, images))
            imageController.insertMany(images)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True, help="folder path to insert in database")
    args = vars(ap.parse_args())
    insertDatabase(args)