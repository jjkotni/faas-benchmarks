import threading
import time
import multiprocessing as mp
from random import randint

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

def inputHandler(event):
    number = randint(1,50)
    response = {
        "statusCode": 200,
        "body": {"number":number}
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
    result = inputHandler(event)

    ######################################################
    global incOut
    incOut = result
    ######################################################

def functionWorker(event):
    increment = threading.Thread(target=incWorker, args=[event])
    square    = threading.Thread(target=squareWorker)

    increment.start()
    increment.join()

    square.start()
    square.join()

    return squareOut

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
