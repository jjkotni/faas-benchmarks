import json
import time
import numpy as np

def renderHandler(event):
    print("Start Time: ", str(1000*time.time()))
    body = json.loads(event['body'])
    x = np.array(body['predictions'])

    text = "Top 1 Prediction: " + str(x.argmax()) + str(x.max())
    print(text)

    response = {
        "statusCode": 200,
        "body": json.dumps({'render': text})
    }

    print("End Time: ", str(1000*time.time()))
    return response
