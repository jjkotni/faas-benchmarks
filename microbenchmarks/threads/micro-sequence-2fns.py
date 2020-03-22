import threading
import time
from mpkmemalloc import *

incOut    = {}
squareOut = {}

def squareHandler(event):
    input = event['body']['number']
    output = input*input

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    return response

def incHandler(event):
    input = event['body']['number']
    output = input+1

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    return response

def squareWorker():
    ######################################################
    global incOut
    ######################################################

    result = squareHandler(incOut)

    ######################################################
    global squareOut
    squareOut = result
    ######################################################

def incWorker(event):
    result = incHandler(event)

    ######################################################
    global incOut
    incOut = result
    ######################################################

def main(event):
    #All marked sections are overheads due to our system
    increment = threading.Thread(target=incWorker, args=[event])
    square    = threading.Thread(target=squareWorker)

    increment.start()
    increment.join()

    square.start()
    square.join()

   return squareOut

# if __name__=="__main__":
#     main({'body':{'number':40}})
