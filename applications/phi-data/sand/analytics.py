import spacy
import json
import time
import ast

def timestamp(response, event, startTime, endTime, externalServicesTime):
    stampBegin = 1000*time.time()
    prior = event['duration'] if 'duration' in event else 0
    priorServiceTime = event['externalServicesTime'] if 'externalServicesTime' in event else 0
    response['duration']     = prior + endTime - startTime
    response['workflowEndTime'] = endTime
    response['workflowStartTime'] = event['workflowStartTime'] if 'workflowStartTime' in event else startTime
    priorCost = event['timeStampCost'] if 'timeStampCost' in event else 0
    response['externalServicesTime'] = priorServiceTime + externalServicesTime
    response['timeStampCost'] = priorCost - (stampBegin-1000*time.time())
    return response

def handle(event, context):
    startTime = 1000*time.time()
    externalServicesTime = 0
    nlp = spacy.load("en_core_web_sm")
    spacyLoadTime = 1000*time.time()-startTime
    doc = nlp(event['body']['message'])
    response = {'statusCode': 200, "body":str(doc), "spacyLoadTime":spacyLoadTime}
    endTime = 1000*time.time()
    return timestamp(response, event, startTime, endTime, externalServicesTime)