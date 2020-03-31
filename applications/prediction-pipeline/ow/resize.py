import os
import json
import time

import boto3
import numpy as np
from PIL import Image
from io import BytesIO
import pickle

BUCKET = 'faas-iisc'
FOLDER = 'prediction-pipeline'
IMAGE  = 'image.jpg'
RESIZE_IMAGE = 'resize-image.pickle'

def main(event):
    s3 = boto3.client('s3', aws_access_key_id="AKIAIDWPIMU4IJPMXVZA",
                      aws_secret_access_key="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",
                      region_name="us-east-1")

    file_byte_string = s3.get_object(Bucket = BUCKET, Key = os.path.join(FOLDER, IMAGE))['Body'].read()
    image = Image.open(BytesIO(file_byte_string))

    img = np.array(image.resize((224, 224))).astype(np.float) / 128 - 1
    resize_img = img.reshape(1, 224,224, 3)

    serialized_resize = pickle.dumps(resize_img)
    response = s3.put_object(Bucket = BUCKET, Key = os.path.join(FOLDER, RESIZE_IMAGE), Body = serialized_resize)

    response = {
        "statusCode": 200
    }

    return response
