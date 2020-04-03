try:
  import unzip_requirements
except ImportError:
  pass

import os
import json
import pickle
import boto3
import tensorflow as tf
import numpy as np

FILE_DIR = '/tmp'
BUCKET = os.environ['BUCKET']
FOLDER = os.environ['FOLDER']
MODEL  = os.environ['MODEL']
RESIZE_IMAGE = os.environ['RESIZE_IMAGE']

def predictHandler(event, context):
    #Use S3 to communicate big messages
    #######################################################################################################################
    BUCKET = 'faas-iisc'
    FOLDER = 'prediction-pipeline'
    RESIZE_IMAGE = 'resize-image.pickle'
    s3 = boto3.client('s3', aws_access_key_id="AKIA3FFYAI3OUV5UWTKJ",
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
    # boto3.Session(
    #     ).resource('s3'
    #     ).Bucket(BUCKET
    #     ).download_file(
    #         os.path.join(FOLDER,    MODEL),
    #         os.path.join(FILE_DIR,  MODEL))

    # boto3.Session(
    #     ).resource('s3'
    #     ).Bucket(BUCKET
    #     ).download_file(
    #         os.path.join(FOLDER,   RESIZE_IMAGE),
    #         os.path.join(FILE_DIR, RESIZE_IMAGE))

    # img  = np.load(os.path.join(FILE_DIR, RESIZE_IMAGE))

    # graph_file = open(os.path.join(FILE_DIR,  MODEL), "rb")

    # gd = tf.GraphDef.FromString(graph_file.read())
    # inp, predictions = tf.import_graph_def(gd,  return_elements = ['input:0', 'MobilenetV2/Predictions/Reshape_1:0'])

    # with tf.Session(graph=inp.graph):
    #     x = predictions.eval(feed_dict={inp: img})

    # response = {
    #     "statusCode": 200,
    #     "body": json.dumps({'predictions': x.tolist()})
    # }

    # return response
