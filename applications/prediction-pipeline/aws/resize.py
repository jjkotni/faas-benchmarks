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
import pickle

FILE_DIR = '/tmp'
BUCKET = os.environ['BUCKET']
FOLDER = os.environ['FOLDER']
IMAGE  = os.environ['IMAGE']
RESIZE_IMAGE = os.environ['RESIZE_IMAGE']

def resizeHandler(event, context):
    image = Image.open("data/image.jpg")
    img = np.array(image.resize((224, 224))).astype(np.float) / 128 - 1
    resize_img = img.reshape(1, 224,224, 3)

    #Baseline allows 1MB messages to be shared, use S3 to communicate messages
    #######################################################################################################################
    serialized_resize = pickle.dumps(resize_img)
    s3 = boto3.client('s3', aws_access_key_id="AKIAIIA72V5T7TZMS33A",
                      aws_secret_access_key="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",
                      region_name="us-east-1")

    BUCKET = 'faas-iisc'
    FOLDER = 'prediction-pipeline'
    RESIZE_IMAGE = 'resize-image.pickle'
    s3response = s3.put_object(Bucket = BUCKET, Key = os.path.join(FOLDER, RESIZE_IMAGE), Body = serialized_resize)
    #######################################################################################################################
    response = {"statusCode": 200}
    # boto3.Session(
    #     ).resource('s3'
    #     ).Bucket(BUCKET
    #     ).download_file(
    #         os.path.join(FOLDER,   IMAGE),
    #         os.path.join(FILE_DIR, IMAGE))

    # img = np.array(Image.open(os.path.join(FILE_DIR, IMAGE)).resize((224, 224))).astype(np.float) / 128 - 1
    # resize_img = img.reshape(1, 224,224, 3)

    # np.save(os.path.join(FILE_DIR, RESIZE_IMAGE), resize_img)

    # boto3.Session(
    #     ).resource('s3'
    #     ).Bucket(BUCKET
    #     ).Object(os.path.join(FOLDER, RESIZE_IMAGE)
    #     ).upload_file(os.path.join(FILE_DIR, RESIZE_IMAGE))

    # response = {
    #     "statusCode": 200
    # }

    return response
