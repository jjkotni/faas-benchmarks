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


def reminderHandler(event, response):
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

def incWorker(input_dict, output_dict):
    incHandler(input_dict, output_dict)

def squareWorker(input_dict, output_dict):
    squareHandler(input_dict, output_dict)

def halfWorker(input_dict, output_dict):
    halfHandler(input_dict, output_dict)

def reminderWorker(input_dict, output_dict):
    reminderHandler(input_dict, output_dict)            


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

        increment_dict = manager.dict()
        increment = Process(target=incWorker, args = (input_dict, increment_dict))
        increment.start()
        increment.join()

        square_dict = manager.dict()
        square = Process(target=squareWorker, args = (increment_dict, square_dict))
        square.start()
        square.join()

        half_dict = manager.dict()
        half = Process(target=halfWorker, args = (square_dict, half_dict))
        half.start()
        half.join()

        reminder_dict = manager.dict()
        reminder = Process(target=reminderWorker, args = (half_dict, reminder_dict))
        reminder.start()
        reminder.join()

        output = dict(reminder_dict)

    return output

if __name__=="__main__":
    print(main({}))
