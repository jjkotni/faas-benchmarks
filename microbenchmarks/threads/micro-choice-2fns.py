import threading
import time
from random import randint

inOut     = {}
divideOut = {}
choiceOut = {}

def inputHandler(event):
    startTime = 1000*time.time()
    number = randint(1,50)
    response = {
        "statusCode": 200,
        "body": {"number":number}
    }

    priorDuration = event['duration'] if 'duration' in event else 0
    response['duration']=priorDuration -(startTime-1000*time.time())
    return response

def incHandler(event):
    startTime = 1000*time.time()
    input = event['body']['number']
    output = input+1

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    priorDuration = event['duration'] if 'duration' in event else 0
    response['duration']=priorDuration -(startTime-1000*time.time())
    return response

def doubleHandler(event):
    startTime = 1000*time.time()
    input = event['body']['number']
    output = 2*input

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    priorDuration = event['duration'] if 'duration' in event else 0
    response['duration']=priorDuration -(startTime-1000*time.time())
    return response

def divideby2Handler(event):
    startTime = 1000*time.time()
    input = event['body']['number']
    output = input%2

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    priorDuration = event['duration'] if 'duration' in event else 0
    response['duration']=priorDuration -(startTime-1000*time.time())
    return response

def inWorker(event):
    result = inputHandler(event)

    ######################################################
    global inOut
    inOut = result
    ######################################################

def divideby2Worker():
    ######################################################
    global inOut
    ######################################################

    result = divideby2Handler(inOut)

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

def doubleWorker():
    ######################################################
    global divideOut
    ######################################################

    result = doubleHandler(divideOut)

    ######################################################
    global choiceOut
    choiceOut = result
    ######################################################

def main(event):
    #All marked sections are overheads due to our system
    input     = threading.Thread(target=inWorker, args = [event])
    divideby2 = threading.Thread(target=divideby2Worker)

    input.start()
    input.join()

    divideby2.start()
    divideby2.join()

    choices = {
        0: incWorker,
        1: doubleWorker
    }

    reminder     = divideOut['body']['number']
    choiceWorker = choices.get(reminder)

    choice    = threading.Thread(target=choiceWorker)

    choice.start()
    choice.join()

    return choiceOut

# if __name__=="__main__":
#     print(main({}))
