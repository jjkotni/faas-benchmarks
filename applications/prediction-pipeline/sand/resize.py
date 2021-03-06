import json
import numpy as np
from PIL import Image
import pickle
import os

def handle(event, context):
    startTime = 1000*time.time()
    image = Image.open("data/image.jpg")
    img = np.array(image.resize((224, 224))).astype(np.float) / 128 - 1
    resize_img = img.reshape(1, 224,224, 3)

    serialized_resize = pickle.dumps(resize_img)

    # Put the object in private object store
    context.put('resized_image', serialized_resize, True)
    #Message passing through shared allows sharing on large objects
    resized = json.dumps(resize_img.tolist())
    response = {
        "statusCode": 200,
        "body": {
            "image": resized
        }
    }
    priorWorkflowDuration = event['duration'] if 'duration' in event else 0
    #Obscure code, doing this to time.time() as late in the function as possible for end time
    response['duration'] = priorWorkflowDuration - (startTime-1000*time.time())
    return response
