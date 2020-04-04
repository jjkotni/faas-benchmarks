import json
import numpy as np
import time
from PIL import Image

def resizeHandler(event):
    print("Start Time: ", str(1000*time.time()))
    image = Image.open("data/image.jpg")
    img = np.array(image.resize((224, 224))).astype(np.float) / 128 - 1
    resize_img = img.reshape(1, 224,224, 3)

    #Message passing through shared allows sharing on large objects
    resized = json.dumps(resize_img.tolist())
    response = {
        "statusCode": 200,
        "body": {
            "image": resized
        }
    }

    print("End Time: ", str(1000*time.time()))
    return response
