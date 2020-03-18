import os
import json
import base64
import boto3
from PIL import Image

FILE_DIR = '/tmp'
IMAGE  = os.environ['IMAGE']
FOLDER = os.environ['FOLDER']
BUCKET = os.environ['BUCKET']

def rotate(image):
    path_list = []
    imgName = "rotate-90-" + IMAGE
    img = image.transpose(Image.ROTATE_90)
    img.save(os.path.join(FILE_DIR,imgName))
    path_list.append(imgName)

    imgName = "rotate-180-" + IMAGE
    img = image.transpose(Image.ROTATE_180)
    img.save(os.path.join(FILE_DIR,imgName))
    path_list.append(imgName)

    imgName = "rotate-270-" + IMAGE
    img = image.transpose(Image.ROTATE_270)
    img.save(os.path.join(FILE_DIR,imgName))
    path_list.append(imgName)

    return path_list

def getImage(body):
    imageString = base64.decodestring(body['image'].encode("utf-8"))
    imageFile = open(os.path.join(FILE_DIR, IMAGE), "wb")
    imageFile.write(imageString)
    imageFile.close()
    image = Image.open(os.path.join(FILE_DIR, IMAGE))
    return image

def rotateHandler(event, context):
    image  = getImage(event['body'])
    images = rotate(image)

    processed = []
    for modImage in images:
        boto3.client('s3').upload_file(os.path.join(FILE_DIR, modImage),
                                       BUCKET,
                                       os.path.join(FOLDER,   modImage))

        processed.append(modImage)

    response = {
        "statusCode": 200,
        "body": {"processedImages": processed}
    }

    return response
