import os
import argparse
from database.controllers.folders_controller import FoldersController
from database.controllers.images_controller import ImagesController


def insertDatabase(args):
    root = args["path"]
    rootFolders = tuple(map(lambda x: os.path.join(root, x), os.listdir(root)))
    folders_paths = tuple(x for x in rootFolders if os.path.isdir(x))
    folders_names = tuple(x for x in os.listdir(root) if os.path.isdir(os.path.join(root, x)))
    
    folderController = FoldersController()
    imageController = ImagesController()

    for name, path in zip(folders_names, folders_paths):
        folder = folderController.getByName(name)
        if folder:
            continue
        folderDict = {
            "name": name,
            "path": path,
            "user_id": None
        }
        fId = folderController.insert(folderDict)

        images = [img for img in os.listdir(path) if os.path.isfile(img) and img.endswith('jpg')]
        images = list(map(lambda img: {"name": img,
                "path": os.path.join(path, img),
                "folder": fId, "processed":False}, images))
        imageController.insertMany(images)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True, help="folder path to insert in database")
    args = vars(ap.parse_args())
    insertDatabase(args)