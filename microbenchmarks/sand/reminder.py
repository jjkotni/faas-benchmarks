#!/usr/bin/python
import json
import time

def handle(event, context):
    startTime = 1000*time.time()
    input = event['body']['number']
    output = input%2

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    priorDuration = event['duration'] if 'duration' in event else 0
    response['duration']=priorDuration -(startTime-1000*time.time())
    return response

# if __name__ == "__main__":
#     response = squareHandler({"body":{"number":2}}, {})
#     print(response)
