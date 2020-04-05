import threading
import time
from random import randint
from mpkmemalloc import *

inOut     = {}
incOut    = {}
squareOut = {}
halfOut   = {}
remOut    = {}
aggOut    = {}
doubleOut = {}

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

def halfHandler(event):
    startTime = 1000*time.time()
    input = event['body']['number']
    output = int(input/2)

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    priorDuration = event['duration'] if 'duration' in event else 0
    response['duration']=priorDuration -(startTime-1000*time.time())
    return response

def reminderHandler(event):
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

def incWorker():
    ######################################################
    tname = threading.currentThread().getName()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    global inOut
    ######################################################

    result = incHandler(inOut)

    ######################################################
    global incOut
    incOut = result
    pymem_reset(tname)
    ######################################################

def squareWorker():
    ######################################################
    tname = threading.currentThread().getName()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    global inOut
    ######################################################

    result = squareHandler(inOut)

    ######################################################
    global squareOut
    squareOut = result
    pymem_reset(tname)
    ######################################################

def halfWorker():
    ######################################################
    tname = threading.currentThread().getName()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    global inOut
    ######################################################

    result = halfHandler(inOut)

    ######################################################
    global halfOut
    halfOut = result
    pymem_reset(tname)
    ######################################################

def remWorker():
    ######################################################
    tname = threading.currentThread().getName()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    global inOut
    ######################################################

    result = reminderHandler(inOut)

    ######################################################
    global remOut
    remOut = result
    pymem_reset(tname)
    ######################################################

def doubleWorker():
    ######################################################
    tname = threading.currentThread().getName()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    global inOut
    ######################################################

    result = doubleHandler(inOut)

    ######################################################
    global doubleOut
    doubleOut = result
    pymem_reset(tname)
    ######################################################

def aggregateWorker():
    ######################################################
    tname = threading.currentThread().getName()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    global incOut, squareOut, remOut, halfOut, doubleOut
    ######################################################

    result = aggregateHandler([incOut, squareOut,
                            remOut, halfOut, doubleOut])

    ######################################################
    global aggOut
    aggOut = result
    pymem_reset(tname)
    ######################################################

def main(event):
    #All marked sections are overheads due to our system
    ######################################################
    pymem_setup_allocators(0)
    ######################################################

    input     = threading.Thread(target=inWorker, args = [event])
    increment = threading.Thread(target=incWorker)
    square    = threading.Thread(target=squareWorker)
    half      = threading.Thread(target=halfWorker)
    reminder  = threading.Thread(target=remWorker)
    double    = threading.Thread(target=doubleWorker)
    aggregate = threading.Thread(target=aggregateWorker)

    input.start()
    input.join()

    #Stupidity!
    # increment.start()
    # increment.join()
    # square.start()
    # square.join()
    # half.start()
    # half.join()
    # reminder.start()
    # reminder.join()
    # double.start()
    # double.join()

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

    ######################################################
    pymem_reset_pkru()
    ######################################################
    return aggOut

# if __name__=="__main__":
#     print(main({}))
