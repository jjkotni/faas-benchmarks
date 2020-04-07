import threading
import time
from random import randint

inOut     = {}
incOut    = {}
squareOut = {}
halfOut   = {}
remOut    = {}

def timestamp(response, event, startTime, endTime):
    stampBegin = 1000*time.time()
    prior = event['duration'] if 'duration' in event else 0
    response['duration']     = prior + endTime - startTime
    response['workflowEndTime'] = endTime
    response['workflowStartTime'] = event['workflowStartTime'] if 'workflowStartTime' in event else startTime
    priorCost = event['timeStampCost'] if 'timeStampCost' in event else 0
    response['timeStampCost'] = priorCost - (stampBegin-1000*time.time())
    return response

def inputHandler(event):
    startTime = 1000*time.time()
    number = randint(1,50)
    response = {
        "statusCode": 200,
        "body": {"number":number}
    }

    endTime = 1000*time.time()
    return timestamp(response, event, startTime, endTime)

def incHandler(event):
    startTime = 1000*time.time()
    input = event['body']['number']
    output = input+1

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    endTime = 1000*time.time()
    return timestamp(response, event, startTime, endTime)

def squareHandler(event):
    startTime = 1000*time.time()
    input = event['body']['number']
    output = input*input

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    endTime = 1000*time.time()
    return timestamp(response, event, startTime, endTime)

def halfHandler(event):
    startTime = 1000*time.time()
    input = event['body']['number']
    output = int(input/2)

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    endTime = 1000*time.time()
    return timestamp(response, event, startTime, endTime)

def reminderHandler(event):
    startTime = 1000*time.time()
    input = event['body']['number']
    output = input%2

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    endTime = 1000*time.time()
    return timestamp(response, event, startTime, endTime)

def inWorker(event):
    result = inputHandler(event)

    ######################################################
    global inOut
    inOut = result
    ######################################################

def incWorker():
    ######################################################
    global inOut
    ######################################################

    result = incHandler(inOut)

    ######################################################
    global incOut
    incOut = result
    ######################################################

def squareWorker():
    ######################################################
    global incOut
    ######################################################

    result = squareHandler(incOut)

    ######################################################
    global squareOut
    squareOut = result
    ######################################################

def halfWorker():
    ######################################################
    global squareOut
    ######################################################

    result = halfHandler(squareOut)

    ######################################################
    global halfOut
    halfOut = result
    ######################################################

def remWorker():
    ######################################################
    global halfOut
    ######################################################

    result = reminderHandler(halfOut)

    ######################################################
    global remOut
    remOut = result
    ######################################################

def main(event):
    #All marked sections are overheads due to our system
    input     = threading.Thread(target=inWorker, args = [event])
    increment = threading.Thread(target=incWorker)
    square    = threading.Thread(target=squareWorker)
    half      = threading.Thread(target=halfWorker)
    reminder  = threading.Thread(target=remWorker)

    input.start()
    input.join()

    increment.start()
    increment.join()

    square.start()
    square.join()

    half.start()
    half.join()

    reminder.start()
    reminder.join()

    return remOut

# if __name__=="__main__":
#     print(main({}))
