#!/usr/bin/python
import json
from random import randint
import time

def handle(event, context):
    startTime = 1000*time.time()
    print(startTime)
    context.put('workflowStartTime', str(startTime), True)
    number = randint(1,50)
    response = {
        "statusCode": 200,
        "body": {"number":number}
    }

    priorDuration = event['duration'] if 'duration' in event else 0
    response['duration']=priorDuration -(startTime-1000*time.time())
    return response

