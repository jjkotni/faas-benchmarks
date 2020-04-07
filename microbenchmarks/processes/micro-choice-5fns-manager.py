from multiprocessing import Process, Manager
import time
from random import randint

def inputHandler(event, response):
    startTime = 1000*time.time()
    number = randint(1,50)

    response["statusCode"] = 200
    response["number"] = number

    priorDuration = event['duration'] if 'duration' in event else 0
    response['duration']=priorDuration - (startTime-1000*time.time())


def divideby5Handler(event, response):
    startTime = 1000*time.time()
    input = event['number']
    output = input%5

    response["statusCode"] = 200
    response["number"] = output

    priorDuration = event['duration'] if 'duration' in event else 0
    response['duration']=priorDuration - (startTime-1000*time.time())


def incHandler(event, response):
    startTime = 1000*time.time()
    input = event['number']
    output = input+1

    response["statusCode"] = 200
    response["number"] = output

    priorDuration = event['duration'] if 'duration' in event else 0
    response['duration']=priorDuration - (startTime-1000*time.time())


def squareHandler(event, response):
    startTime = 1000*time.time()
    input = event['number']
    output = input*input

    response["statusCode"] = 200
    response["number"] = output

    priorDuration = event['duration'] if 'duration' in event else 0
    response['duration']=priorDuration - (startTime-1000*time.time())


def halfHandler(event, response):
    startTime = 1000*time.time()
    input = event['number']
    output = int(input/2)

    response["statusCode"] = 200
    response["number"] = output

    priorDuration = event['duration'] if 'duration' in event else 0
    response['duration']=priorDuration - (startTime-1000*time.time())


def doubleHandler(event, response):
    startTime = 1000*time.time()
    input = event['number']
    output = 2*input

    response["statusCode"] = 200
    response["number"] = output

    priorDuration = event['duration'] if 'duration' in event else 0
    response['duration']=priorDuration - (startTime-1000*time.time())


def divideby2Handler(event, response):
    startTime = 1000*time.time()
    input = event['number']
    output = input%2

    response["statusCode"] = 200
    response["number"] = output

    priorDuration = event['duration'] if 'duration' in event else 0
    response['duration']=priorDuration - (startTime-1000*time.time())


###############################################################################
###############################################################################


def inWorker(input_dict, output_dict):
    inputHandler(input_dict, output_dict)

def divideby5Worker(input_dict, output_dict):
    divideby5Handler(input_dict, output_dict) 

def incWorker(input_dict, output_dict):
    incHandler(input_dict, output_dict)

def squareWorker(input_dict, output_dict):
    squareHandler(input_dict, output_dict)

def halfWorker(input_dict, output_dict):
    halfHandler(input_dict, output_dict)

def doubleWorker(input_dict, output_dict):
    doubleHandler(input_dict, output_dict) 

def divideby2Worker(input_dict, output_dict):
    divideby2Handler(input_dict, output_dict) 


###############################################################################
###############################################################################


def main(event):
    ''' main function is our orchestrator!
    The first function of the workflow needs input and a shared dict to return
    response. The reminder of the functions needs atleast 2 arguments, the response
    from previous function and a new one for it's own response. The response that
    returns from the last function is copied to an output dict and be done retured!
    '''
    output = None
    with Manager() as manager:
        input_dict = manager.dict()
        input = Process(target=inWorker, args = (event, input_dict))
        input.start()
        input.join()

        divide5_dict = manager.dict()
        divide5 = Process(target=divideby5Worker, args = (input_dict, divide5_dict))
        divide5.start()
        divide5.join()

        choices = {
            0: squareWorker,
            1: incWorker,
            2: divideby2Worker,
            3: doubleWorker,
            4: halfWorker
        }

        reminder     = divide5_dict['number']
        choiceWorker = choices.get(reminder)

        choice_dict = manager.dict()
        choice = Process(target=choiceWorker, args = (divide5_dict, choice_dict))
        choice.start()
        choice.join()

        output = dict(choice_dict)

    return output

if __name__=="__main__":
    print(main({}))
