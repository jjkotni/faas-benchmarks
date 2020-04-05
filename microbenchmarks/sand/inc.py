#!/usr/bin/python
import time
import json

def handle(event, context):
    startTime = 1000*time.time()
    input = event['body']['number']
    output = input+1

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    priorDuration = event['duration'] if 'duration' in event else 0
    workflowStartTime = context.get('workflowStartTime', True)
    workflowStartTime = float(workflowStartTime) if workflowStartTime != "" else startTime
    endTime = 1000*time.time()
    response['duration']     = priorDuration + endTime - startTime
    response['totalRunTime'] = endTime - workflowStartTime
    return response
