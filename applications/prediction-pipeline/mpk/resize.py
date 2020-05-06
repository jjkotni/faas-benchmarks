import json
import numpy as np
import time
from PIL import Image
from mpkmemalloc import *
from util import *

def resizeHandler(event):
    startTime = 1000*time.time()
    image = Image.open("data/image.jpg")
    img = np.array(image.resize((224, 224))).astype(np.float) / 128 - 1
    resize_img = img.reshape(1, 224,224, 3)

    #Message passing through shared allows sharing on large objects
    resized = json.dumps(resize_img.tolist())
    # pymem_allocate_from_shmem()
    response = {
        "statusCode": 200,
        "body": {
            "image": resized
        }
    }

    endTime = 1000*time.time()
    return timestamp(response, event, startTime, endTime, 0)

# if __name__ == "__main__":
#     resizeHandler({})
