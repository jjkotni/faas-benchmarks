import os
import json
import base64

import boto3

FILE_DIR = '/tmp'
BUCKET = os.environ['BUCKET']
FOLDER = os.environ['FOLDER']
IMAGE  = os.environ['IMAGE']

def fetchHandler(event, context):
    boto3.Session(
        ).resource('s3'
        ).Bucket(BUCKET
        ).download_file(
            os.path.join(FOLDER,   IMAGE),
            os.path.join(FILE_DIR, IMAGE))

    img = open(os.path.join(FILE_DIR, IMAGE), 'rb')
    img_encode = base64.b64encode(img.read()).decode("utf-8")

    response = {
        "statusCode": 200,
        "body": {"image": img_encode}
    }

    return response
