import threading
import time
from random import randint

inOut     = {}
incOut    = {}
squareOut = {}
aggOut    = {}

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

def squareHandler(event):
    startTime = 1000*time.time()
    input = event['body']['number']
    output = input*input

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    priorDuration = event['duration'] if 'duration' in event else 0
    response['duration']=priorDuration -(startTime-1000*time.time())
    return response

def aggregateHandler(events):
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
    response['duration']=priorDuration -(startTime-1000*time.time())
    return response

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
    global inOut
    ######################################################

    result = squareHandler(inOut)

    ######################################################
    global squareOut
    squareOut = result
    ######################################################

def aggregateWorker():
    ######################################################
    global incOut, squareOut
    ######################################################

    result = aggregateHandler([incOut, squareOut])

    ######################################################
    global aggOut
    aggOut = result
    ######################################################

def main(event):
    #All marked sections are overheads due to our system
    input     = threading.Thread(target=inWorker, args = [event])
    increment = threading.Thread(target=incWorker)
    square    = threading.Thread(target=squareWorker)
    aggregate = threading.Thread(target=aggregateWorker)

    input.start()
    input.join()

    #Parallel Functions
    increment.start()
    square.start()

    square.join()
    increment.join()

    aggregate.start()
    aggregate.join()

    return aggOut

# if __name__=="__main__":
#     print(main({}))
