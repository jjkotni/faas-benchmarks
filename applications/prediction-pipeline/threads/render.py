import json
import time
import numpy as np
from util import *

def renderHandler(event):
    startTime = 1000*time.time()
    body = json.loads(event['body'])
    x = np.array(body['predictions'])

    text = "Top 1 Prediction: " + str(x.argmax()) + str(x.max())
    print(text)

    response = {
        "statusCode": 200,
        "body": json.dumps({'render': text})
    }

    endTime = 1000*time.time()
    return timestamp(response, event, startTime, endTime, 0)
