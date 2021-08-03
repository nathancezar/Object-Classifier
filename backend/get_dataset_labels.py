import os
import shutil
import re
import tarfile
import time
from database.controllers.images_controller import ImagesController
from database.controllers.labels_controller import LabelsController

WIDTH = 1920
HEIGHT = 1080

def formatLabels(args, label):
    if args["format"] == "yolo":
        xCenter = label["x_center"] / WIDTH
        yCenter = label["y_center"] / HEIGHT
        width = label["width"] / WIDTH
        height = label["height"] / HEIGHT
        return f'{label["item_id"]} {xCenter} {yCenter} {width} {height} \n'
    elif args["format"] == "faster":
        x0 = int(label["x_center"] - (label["width"] / 2))
        x1 = int(label["x_center"] + (label["width"] / 2))
        y0 = int(label["y_center"] - (label["height"] / 2))
        y1 = int(label["y_center"] + (label["height"] / 2))
        return f'{label["item_id"]} {x0} {y0} {x1} {y1} \n'

def exportFolder(args):
    images, labels = export(args["folder"], args)
    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
    filename = f'{args["tar_out"]}/{args["folder"]["name"]}_{args["format"]}_{timestamp}.tar.gz'
    saveTarfile(filename, images, labels)

def exportAll(args, extra=""):
    images = []
    labels = []
    for folder in args["folders"]:
        filenames = export(folder, args)
        images += filenames[0]
        labels += filenames[1]
    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
    filename = f'{args["tar_out"]}/{args["format"]}_{timestamp}.tar.gz'
    saveTarfile(filename, images, labels)

def export(folder, args):
    labelsOut = f'{args["labels_out"]}/{folder["name"]}_{{0}}.txt'
    imagesController = ImagesController()
    labelsController = LabelsController()
    imageFilenames = []
    labelFilenames = []

    images = imagesController.getAllByFolderId(folder["id"], processed=True)

    for image in images:
        labels = labelsController.getAllByImageId(image["id"])
        if labels:
            labelFilename = labelsOut.format(re.sub("\.jpg$", "", image["name"]))
            labelFilenames.append(labelFilename)
            with open(labelFilename, "w") as labelFile:
                for label in labels:
                    labelFile.write(formatLabels(args, label))
            imageIn = f'{folder["path"]}/{image["name"]}'
            imageOut = f'{args["images_out"]}/{folder["name"]}_{image["name"]}'
            shutil.copyfile(imageIn, imageOut)
            imageFilenames.append(imageOut)
    return imageFilenames, labelFilenames

def exportByType(args):
    labelsOut = f'{args["labels_out"]}/{{0}}_{{1}}.txt'
    imagesController = ImagesController()
    labelsController = LabelsController()
    labels = []
    for itemId in args["items"]:
        labels += labelsController.getAllByItemId(itemId)
    images = {}
    for label in labels:
        if label["image_id"] not in images:
            images[label["image_id"]] = []
        images[label["image_id"]].append(label)
    imageFilenames = []
    labelFilenames = []
    for imageId in images:
        image = imagesController.getById(int(imageId))
        if image:
            folderName = image["path"].split("/")[-2]
            labelFilename = labelsOut.format(folderName, re.sub("\.jpg$", "", image["name"]))
            labelFilenames.append(labelFilename)
            with open(labelFilename, "w") as labelFile:
                for label in images[imageId]:
                    labelFile.write(formatLabels(args, label))
            imageOut = f'{args["images_out"]}/{folderName}_{image["name"]}'
            shutil.copyfile(image["path"], imageOut)
            imageFilenames.append(imageOut)
    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
    filename = f'{args["tar_out"]}/{args["format"]}_{timestamp}.tar.gz'
    saveTarfile(filename, imageFilenames, labelFilenames)

def saveTarfile(filename, images, labels):
    with tarfile.open(filename, "w:gz") as tarFile:
        for image in images: tarFile.add(image, arcname=f'images/{os.path.basename(image)}')
        for label in labels: tarFile.add(label, arcname=f'labels/{os.path.basename(label)}')
