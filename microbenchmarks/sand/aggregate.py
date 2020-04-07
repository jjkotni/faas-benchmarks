#!/usr/bin/python
import json
import time

def timestamp(response, events, startTime, endTime):
    stampBegin = 1000*time.time()
    prior = 0
    priorCost = 0
    workflowStartTime = startTime
    for event in events:
        if 'duration' in event and event['duration'] > prior:
            prior = event['duration']
            #Pick timestamp costs from the same event/path
            priorCost = event['timeStampCost'] if 'timeStampCost' in event else 0
        if 'workflowStartTime' in event and event['workflowStartTime'] < workflowStartTime:
            workflowStartTime = event['workflowStartTime']

    response['duration']     = prior + endTime - startTime
    response['workflowEndTime'] = endTime
    response['workflowStartTime'] = workflowStartTime

    #Obscure code, doing to time.time() at the end of fn
    response['timeStampCost'] = priorCost - (stampBegin-1000*time.time())
    return response

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

    endTime = 1000*time.time()
    return timestamp(response, events, startTime, endTime)

