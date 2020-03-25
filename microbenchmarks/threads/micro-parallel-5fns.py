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
    print("Start Time: ", str(1000*time.time()))
    number = randint(1,50)
    response = {
        "statusCode": 200,
        "body": {"number":number}
    }

    print("End Time: ", str(1000*time.time()))
    return response

def incHandler(event):
    print("Start Time: ", str(1000*time.time()))
    input = event['body']['number']
    output = input+1

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    print("End Time: ", str(1000*time.time()))
    return response

def squareHandler(event):
    print("Start Time: ", str(1000*time.time()))
    input = event['body']['number']
    output = input*input

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    print("End Time: ", str(1000*time.time()))
    return response

def halfHandler(event):
    print("Start Time: ", str(1000*time.time()))
    input = event['body']['number']
    output = int(input/2)

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    print("End Time: ", str(1000*time.time()))
    return response

def reminderHandler(event):
    print("Start Time: ", str(1000*time.time()))
    input = event['body']['number']
    output = input%2

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    print("End Time: ", str(1000*time.time()))
    return response

def doubleHandler(event):
    print("Start Time: ", str(1000*time.time()))
    input = event['body']['number']
    output = 2*input

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    print("End Time: ", str(1000*time.time()))
    return response

def aggregateHandler(events):
    print("Start Time: ", str(1000*time.time()))
    aggregate = 0
    for event in events:
        aggregate += event['body']['number']

    response = {
        "statusCode": 200,
        "body":{"number":aggregate}
    }

    print("End Time: ", str(1000*time.time()))
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

if __name__=="__main__":
    main({})
