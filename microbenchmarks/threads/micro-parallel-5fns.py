import threading
import time
from random import randint

inOut     = {}
incOut    = {}
squareOut = {}
halfOut   = {}
remOut    = {}
aggOut    = {}
doubleOut = {}

def agg_timestamp(response, events, startTime, endTime):
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

    endTime = 1000*time.time()
    return agg_timestamp(response, events, startTime, endTime)

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

def halfWorker():
    ######################################################
    global inOut
    ######################################################

    result = halfHandler(inOut)

    ######################################################
    global halfOut
    halfOut = result
    ######################################################

def remWorker():
    ######################################################
    global inOut
    ######################################################

    result = reminderHandler(inOut)

    ######################################################
    global remOut
    remOut = result
    ######################################################

def doubleWorker():
    ######################################################
    global inOut
    ######################################################

    result = doubleHandler(inOut)

    ######################################################
    global doubleOut
    doubleOut = result
    ######################################################

def aggregateWorker():
    ######################################################
    global incOut, squareOut, remOut, halfOut, doubleOut
    ######################################################

    result = aggregateHandler([incOut, squareOut,
                            remOut, halfOut, doubleOut])

    ######################################################
    global aggOut
    aggOut = result
    ######################################################

def main(event):
    #All marked sections are overheads due to our system
    input     = threading.Thread(target=inWorker, args = [event])
    increment = threading.Thread(target=incWorker)
    square    = threading.Thread(target=squareWorker)
    half      = threading.Thread(target=halfWorker)
    reminder  = threading.Thread(target=remWorker)
    double    = threading.Thread(target=doubleWorker)
    aggregate = threading.Thread(target=aggregateWorker)

    input.start()
    input.join()

    #Parallel Functions
    increment.start()
    square.start()
    half.start()
    reminder.start()
    double.start()

    reminder.join()
    half.join()
    square.join()
    increment.join()
    double.join()

    aggregate.start()
    aggregate.join()

    # print(inOut)
    # print(incOut)
    # print(squareOut)
    # print(remOut)
    # print(halfOut)
    # print(doubleOut)
    # print(aggOut)

    return aggOut

# if __name__=="__main__":
#     print(main({}))
