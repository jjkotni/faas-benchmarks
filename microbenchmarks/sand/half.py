#!/usr/bin/python
import time
import json

def timestamp(response, event, startTime, endTime):
    stampBegin = 1000*time.time()
    workflowStartTime = event['workflowStartTime'] if 'workflowStartTime' in event else startTime
    prior = event['duration'] if 'duration' in event else 0
    priorCost = event['timeStampCost'] if 'timeStampCost' in event else 0
    response['workflowStartTime'] = workflowStartTime
    response['workflowEndTime'] = endTime
    response['duration'] = prior + endTime - startTime
    response['timeStampCost'] = priorCost - (stampBegin-1000*time.time())
    return response

def handle(event, context):
    startTime = 1000*time.time()
    input = event['body']['number']
    output = int(input/2)

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    endTime = 1000*time.time()
    return timestamp(response, event, startTime, endTime)

# if __name__ == "__main__":
#     response = squareHandler({"body":{"number":3}}, {})
#     print(response)
