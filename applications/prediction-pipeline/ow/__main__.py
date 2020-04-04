import os
import json
import boto3
import pickle
import numpy as np
import tensorflow as tf

def main(event):
    #Use S3 to communicate big messages
    #######################################################################################################################
    BUCKET = 'faas-iisc'
    FOLDER = 'prediction-pipeline'
    RESIZE_IMAGE = 'resize-image.pickle'
    s3 = boto3.client('s3', aws_access_key_id="AKIA3FFYAI3ORS6ANNHL",
                      aws_secret_access_key="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", region_name="us-east-1")
    resize_pickle = s3.get_object(Bucket = BUCKET, Key = os.path.join(FOLDER, RESIZE_IMAGE))['Body'].read()
    img = pickle.loads(resize_pickle)
    #######################################################################################################################
    gd = tf.GraphDef.FromString(open('data/mobilenet_v2_1.0_224_frozen.pb', 'rb').read())

    inp, predictions = tf.import_graph_def(gd,  return_elements = ['input:0', 'MobilenetV2/Predictions/Reshape_1:0'])

    with tf.Session(graph=inp.graph):
        x = predictions.eval(feed_dict={inp: img})

    response = {
        "statusCode": 200,
        "body": json.dumps({'predictions': x.tolist()})
    }

    return response
