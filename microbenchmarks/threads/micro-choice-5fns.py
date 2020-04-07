import threading
import time
from random import randint

inOut     = {}
divideOut = {}
choiceOut = {}

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

def doubleHandler(event):
    startTime = 1000*time.time()
    input = event['body']['number']
    output = 2*input

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    endTime = 1000*time.time()
    return timestamp(response, event, startTime, endTime)

def divideby5Handler(event):
    startTime = 1000*time.time()
    input = event['body']['number']
    output = input%5

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    endTime = 1000*time.time()
    return timestamp(response, event, startTime, endTime)

def divideby2Handler(event):
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

def divideby5Worker():
    ######################################################
    global inOut
    ######################################################

    result = divideby5Handler(inOut)

    ######################################################
    global divideOut
    divideOut = result
    ######################################################

def incWorker():
    ######################################################
    global divideOut
    ######################################################

    result = incHandler(divideOut)

    ######################################################
    global choiceOut
    choiceOut = result
    ######################################################

def squareWorker():
    ######################################################
    global divideOut
    ######################################################

    result = squareHandler(divideOut)

    ######################################################
    global choiceOut
    choiceOut = result
    ######################################################

def divideby2Worker():
    ######################################################
    global divideOut
    ######################################################

    result = divideby2Handler(divideOut)

    ######################################################
    global choiceOut
    choiceOut = result
    ######################################################

def doubleWorker():
    ######################################################
    global divideOut
    ######################################################

    result = doubleHandler(divideOut)

    ######################################################
    global choiceOut
    choiceOut = result
    ######################################################

def halfWorker():
    ######################################################
    global divideOut
    ######################################################

    result = halfHandler(divideOut)

    ######################################################
    global choiceOut
    choiceOut = result
    ######################################################

def main(event):
    #All marked sections are overheads due to our system
    input     = threading.Thread(target=inWorker, args = [event])
    divideby5 = threading.Thread(target=divideby5Worker)

    input.start()
    input.join()

    divideby5.start()
    divideby5.join()

    choices = {
        0: squareWorker,
        1: incWorker,
        2: divideby2Worker,
        3: doubleWorker,
        4: halfWorker
    }

    reminder     = divideOut['body']['number']
    choiceWorker = choices[reminder]

    choice    = threading.Thread(target=choiceWorker)

    choice.start()
    choice.join()

    return choiceOut

# if __name__=="__main__":
#     print(main({}))
