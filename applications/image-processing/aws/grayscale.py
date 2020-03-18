import os
import json
import base64
import boto3
from PIL import Image

FILE_DIR = '/tmp'
IMAGE  = os.environ['IMAGE']
FOLDER = os.environ['FOLDER']
BUCKET = os.environ['BUCKET']

def grayscale(image):
    imgName = "gray-scale-" + IMAGE
    img = image.convert('L')
    img.save(os.path.join(FILE_DIR,imgName))
    return [imgName]

def getImage(body):
    imageString = base64.decodestring(body['image'].encode("utf-8"))
    imageFile = open(os.path.join(FILE_DIR, IMAGE), "wb")
    imageFile.write(imageString)
    imageFile.close()
    image = Image.open(os.path.join(FILE_DIR, IMAGE))
    return image

def grayscaleHandler(event, context):
    image  = getImage(event['body'])
    images = grayscale(image)

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
