#!/usr/bin/python
import json
import time

def handle(events, context):
    startTime = 1000*time.time()
    aggregate = 0
    durations = []
    for event in events:
        if 'duration' in event:
            durations.append(event['duration'])
        aggregate += event['body']['number']

    response = {
        "statusCode": 200,
        "body":{"number":aggregate}
    }

    priorDuration = max(durations) if len(durations) else 0
    response['duration']=priorDuration -(starTime-1000*time.time())
    return response

