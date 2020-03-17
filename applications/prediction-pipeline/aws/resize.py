try:
  import unzip_requirements
except ImportError:
  pass

import os
import json
import time

import boto3
import numpy as np
from PIL import Image

FILE_DIR = '/tmp'
BUCKET = os.environ['BUCKET']
FOLDER = os.environ['FOLDER']
IMAGE  = os.environ['IMAGE']
RESIZE_IMAGE = os.environ['RESIZE_IMAGE']

def resizeHandler(event, context):
    boto3.Session(
        ).resource('s3'
        ).Bucket(BUCKET
        ).download_file(
            os.path.join(FOLDER,   IMAGE),
            os.path.join(FILE_DIR, IMAGE))

    img = np.array(Image.open(os.path.join(FILE_DIR, IMAGE)).resize((224, 224))).astype(np.float) / 128 - 1
    resize_img = img.reshape(1, 224,224, 3)

    np.save(os.path.join(FILE_DIR, RESIZE_IMAGE), resize_img)

    boto3.Session(
        ).resource('s3'
        ).Bucket(BUCKET
        ).Object(os.path.join(FOLDER, RESIZE_IMAGE)
        ).upload_file(os.path.join(FILE_DIR, RESIZE_IMAGE))

    response = {
        "statusCode": 200
    }

    return response
