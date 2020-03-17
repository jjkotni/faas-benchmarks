try:
  import unzip_requirements
except ImportError:
  pass

import os
import json

import boto3
import tensorflow as tf
import numpy as np

FILE_DIR = '/tmp'
BUCKET = os.environ['BUCKET']
FOLDER = os.environ['FOLDER']
MODEL  = os.environ['MODEL']
RESIZE_IMAGE = os.environ['RESIZE_IMAGE']

def predictHandler(event, context):
    boto3.Session(
        ).resource('s3'
        ).Bucket(BUCKET
        ).download_file(
            os.path.join(FOLDER,    MODEL),
            os.path.join(FILE_DIR,  MODEL))

    boto3.Session(
        ).resource('s3'
        ).Bucket(BUCKET
        ).download_file(
            os.path.join(FOLDER,   RESIZE_IMAGE),
            os.path.join(FILE_DIR, RESIZE_IMAGE))

    img  = np.load(os.path.join(FILE_DIR, RESIZE_IMAGE))

    graph_file = open(os.path.join(FILE_DIR,  MODEL), "rb")

    gd = tf.GraphDef.FromString(graph_file.read())
    inp, predictions = tf.import_graph_def(gd,  return_elements = ['input:0', 'MobilenetV2/Predictions/Reshape_1:0'])

    with tf.Session(graph=inp.graph):
        x = predictions.eval(feed_dict={inp: img})

    response = {
        "statusCode": 200,
        "body": json.dumps({'predictions': x.tolist()})
    }

    return response
