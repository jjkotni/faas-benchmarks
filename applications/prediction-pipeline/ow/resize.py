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
    s3 = boto3.client('s3', aws_access_key_id="AKIA3FFYAI3ORS6ANNHL",
                      aws_secret_access_key="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",
                      region_name="us-east-1")

    BUCKET = 'faas-iisc'
    FOLDER = 'prediction-pipeline'
    RESIZE_IMAGE = 'resize-image.pickle'
    s3response = s3.put_object(Bucket = BUCKET, Key = os.path.join(FOLDER, RESIZE_IMAGE), Body = serialized_resize)
    #######################################################################################################################
    response = {"statusCode": 200}
    return response
