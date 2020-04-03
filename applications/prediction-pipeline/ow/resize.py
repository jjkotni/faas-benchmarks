import json
import numpy as np
from PIL import Image
import pickle
import boto3
import os

def main(event):
    image = Image.open("data/image.jpg")
    img = np.array(image.resize((224, 224))).astype(np.float) / 128 - 1
    resize_img = img.reshape(1, 224,224, 3)

    #Baseline allows 1MB messages to be shared, use S3 to communicate messages
    #######################################################################################################################
    serialized_resize = pickle.dumps(resize_img)
    s3 = boto3.client('s3', aws_access_key_id="AKIA3FFYAI3OUV5UWTKJ",
                      aws_secret_access_key="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",
                      region_name="us-east-1")

    BUCKET = 'faas-iisc'
    FOLDER = 'prediction-pipeline'
    RESIZE_IMAGE = 'resize-image.pickle'
    s3response = s3.put_object(Bucket = BUCKET, Key = os.path.join(FOLDER, RESIZE_IMAGE), Body = serialized_resize)
    #######################################################################################################################
    response = {"statusCode": 200}
    return response
