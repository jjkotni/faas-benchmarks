import threading
import time
from random import randint
from mpkmemalloc import *

inOut     = {}
squareOut = {}

def inputHandler(event):
    print("Start Time: ", str(1000*time.time()))
    number = randint(1,50)
    response = {
        "statusCode": 200,
        "body": {"number":number}
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

def inWorker(event):
    result = inputHandler(event)

    ######################################################
    global inOut
    inOut = result
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

def main(event):
    #All marked sections are overheads due to our system
    input     = threading.Thread(target=inWorker, args=[event])
    square    = threading.Thread(target=squareWorker)

    input.start()
    input.join()

    square.start()
    square.join()

    return squareOut

# if __name__=="__main__":
#     print(main({}))
