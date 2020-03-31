import os
import json

import boto3
import tensorflow as tf
import numpy as np
import pickle

BUCKET = 'faas-iisc'
FOLDER = 'prediction-pipeline'
RESIZE_IMAGE = 'resize-image.pickle'
MODEL = 'mobilenet_v2_1.0_224_frozen.pb'

def main(event):
    s3 = boto3.client('s3', aws_access_key_id="AKIAIDWPIMU4IJPMXVZA",
                      aws_secret_access_key="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",
                      region_name="us-east-1")

    resize_pickle = s3.get_object(Bucket = BUCKET, Key = os.path.join(FOLDER, RESIZE_IMAGE))['Body'].read()
    img = pickle.loads(resize_pickle)

    model_byte_string = s3.get_object(Bucket = BUCKET, Key = os.path.join(FOLDER, MODEL))['Body'].read()
    gd = tf.GraphDef.FromString(model_byte_string)

    inp, predictions = tf.import_graph_def(gd,  return_elements = ['input:0', 'MobilenetV2/Predictions/Reshape_1:0'])

    with tf.Session(graph=inp.graph):
        x = predictions.eval(feed_dict={inp: img})

    response = {
        "statusCode": 200,
        "body": json.dumps({'predictions': x.tolist()})
    }

    return response
