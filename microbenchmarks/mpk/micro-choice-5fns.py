import threading
import time
from random import randint
from mpkmemalloc import *

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
    ######################################################
    tname = threading.currentThread().getName()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    ######################################################

    result = inputHandler(event)

    ######################################################
    global inOut
    inOut = result
    pymem_reset(tname)
    ######################################################

def divideby5Worker():
    ######################################################
    tname = threading.currentThread().getName()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    global inOut
    ######################################################

    result = divideby5Handler(inOut)

    ######################################################
    global divideOut
    divideOut = result
    pymem_reset(tname)
    ######################################################

def incWorker():
    ######################################################
    tname = threading.currentThread().getName()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    global divideOut
    ######################################################

    result = incHandler(divideOut)

    ######################################################
    global choiceOut
    choiceOut = result
    pymem_reset(tname)
    ######################################################

def squareWorker():
    ######################################################
    tname = threading.currentThread().getName()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    global divideOut
    ######################################################

    result = squareHandler(divideOut)

    ######################################################
    global choiceOut
    choiceOut = result
    pymem_reset(tname)
    ######################################################

def halfWorker():
    ######################################################
    tname = threading.currentThread().getName()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    global divideOut
    ######################################################

    result = halfHandler(divideOut)

    ######################################################
    global choiceOut
    choiceOut = result
    pymem_reset(tname)
    ######################################################

def divideby2Worker():
    ######################################################
    tname = threading.currentThread().getName()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    global divideOut
    ######################################################

    result = divideby2Handler(divideOut)

    ######################################################
    global choiceOut
    choiceOut = result
    pymem_reset(tname)
    ######################################################

def doubleWorker():
    ######################################################
    tname = threading.currentThread().getName()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    global divideOut
    ######################################################

    result = doubleHandler(divideOut)

    ######################################################
    global choiceOut
    choiceOut = result
    pymem_reset(tname)
    ######################################################

def main(event):
    #All marked sections are overheads due to our system
    ######################################################
    pymem_setup_allocators(0)
    ######################################################

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
    choiceWorker = choices.get(reminder)

    choice    = threading.Thread(target=choiceWorker)

    choice.start()
    choice.join()

    ######################################################
    pymem_reset_pkru()
    ######################################################
    return choiceOut

# if __name__=="__main__":
#     print(main({}))
