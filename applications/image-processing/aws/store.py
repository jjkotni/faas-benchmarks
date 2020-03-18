import os
import json
import base64

def storeHandler(event, context):
    if 'ParallelResultPath' in event:
        print(event['ParallelResultPath'])
    else:
        print("ParallelResultPath not found in event :(")
        print(event)

    response = {
        "statusCode": 200
    }

    return response
