import threading
import time
from random import randint
import multiprocessing as mp

inOut     = {}
incOut    = {}
squareOut = {}
halfOut   = {}
remOut    = {}

def inputHandler(event):
    number = randint(1,50)
    response = {
        "statusCode": 200,
        "body": {"number":number}
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

def squareHandler(event):
    input = event['body']['number']
    output = input*input

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    return response

def halfHandler(event):
    input = event['body']['number']
    output = int(input/2)

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    return response

def reminderHandler(event):
    input = event['body']['number']
    output = input%2

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    return response

def inWorker(event):
    ######################################################
    ######################################################

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
    global incOut
    ######################################################

    result = squareHandler(incOut)

    ######################################################
    global squareOut
    squareOut = result
    ######################################################

def halfWorker():
    ######################################################
    global squareOut
    ######################################################

    result = halfHandler(squareOut)

    ######################################################
    global halfOut
    halfOut = result
    ######################################################

def remWorker():
    ######################################################
    global halfOut
    ######################################################

    result = reminderHandler(halfOut)

    ######################################################
    global remOut
    remOut = result
    ######################################################

def functionWorker(event):
    input     = threading.Thread(target=inWorker, args = [event])
    increment = threading.Thread(target=incWorker)
    square    = threading.Thread(target=squareWorker)
    half      = threading.Thread(target=halfWorker)
    reminder  = threading.Thread(target=remWorker)

    input.start()
    input.join()

    increment.start()
    increment.join()

    square.start()
    square.join()

    half.start()
    half.join()

    reminder.start()
    reminder.join()

    return remOut

def processWrapper(activationId, event, responseQueue):
    response = functionWorker(event)

    ######################################################
    responseQueue.put({activationId:response})
    ######################################################

def main(events):
    processes = []
    responseQueue = mp.Queue()

    for activationId, event in events.items():
        processes.append(mp.Process(target=processWrapper, args=[activationId, event, responseQueue]))

    for idx, process in enumerate(processes):
        process.start()

    for idx, process in enumerate(processes):
        process.join()

    result = {}
    for x in range(len(events)):
        result.update(responseQueue.get())

    return(result)

# if __name__ == '__main__':
#     out = main({'activation1':{},'activation3':{},'activation4':{}, 'activation2': {},
#              'activation31':{},'activation33':{},'activation34':{}, 'activation32': {},
#              'activation45':{},'activation46':{},'activation47':{}, 'activation48': {}})
