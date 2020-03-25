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

def main(event):
    #All marked sections are overheads due to our system
    ######################################################
    pymem_setup_allocators(0)
    ######################################################

    input     = threading.Thread(target=inWorker, args=[event])
    square    = threading.Thread(target=squareWorker)

    input.start()
    input.join()

    square.start()
    square.join()

    ######################################################
    pymem_reset_pkru()
    ######################################################
    return squareOut

# if __name__=="__main__":
#     main({})
