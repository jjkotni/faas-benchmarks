import os
import time
import json
import numpy as np
import tensorflow as tf
from util import *

def predictHandler(event):
    startTime = 1000*time.time()
    img = np.array(json.loads(event['body']['image']))

    gd = tf.GraphDef.FromString(open('data/mobilenet_v2_1.0_224_frozen.pb', 'rb').read())

    inp, predictions = tf.import_graph_def(gd,  return_elements = ['input:0', 'MobilenetV2/Predictions/Reshape_1:0'])

    with tf.Session(graph=inp.graph):
        x = predictions.eval(feed_dict={inp: img})

    response = {
        "statusCode": 200,
        "body": json.dumps({'predictions': x.tolist()})
    }

    endTime = 1000*time.time()
    return timestamp(response, event, startTime, endTime, 0)
