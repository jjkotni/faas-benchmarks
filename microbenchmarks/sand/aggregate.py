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
    workflowStartTime = context.get('workflowStartTime', True)
    workflowStartTime = float(workflowStartTime) if workflowStartTime != "" else startTime
    endTime = 1000*time.time()
    response['duration']     = priorDuration + endTime - startTime
    response['totalRunTime'] = endTime - workflowStartTime
    return response

