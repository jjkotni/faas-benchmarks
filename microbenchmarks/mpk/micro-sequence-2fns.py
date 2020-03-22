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
    tname = threading.currentThread().getName()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    global incOut
    ######################################################

    result = squareHandler(incOut)

    ######################################################
    global squareOut
    squareOut = result
    pymem_reset(tname)
    ######################################################

def incWorker(event):
    ######################################################
    tname = threading.currentThread().getName()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    ######################################################

    result = incHandler(event)

    ######################################################
    global incOut
    incOut = result
    pymem_reset(tname)
    ######################################################

def main(event):
    #All marked sections are overheads due to our system
    ######################################################
    pymem_setup_allocators(0)
    ######################################################

    increment = threading.Thread(target=incWorker, args=[event])
    square    = threading.Thread(target=squareWorker)

    increment.start()
    increment.join()

    square.start()
    square.join()

    ######################################################
    pymem_reset_pkru()
    ######################################################

# if __name__=="__main__":
#     main()
