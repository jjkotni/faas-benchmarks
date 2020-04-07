from multiprocessing import Process, Array
import time
from random import randint

STATUS_IDX=0
NUMBER_IDX=1
DURATION_IDX=2
WSTATIME_IDX=3
WENDTIME_IDX=4
TSTACOST_IDX=5

def timestamp (event, response, startTime, endTime):
    stampBegin = 1000*time.time()
    prior = event[DURATION_IDX] if event[DURATION_IDX] > 0 else 0
    response[DURATION_IDX] = prior + endTime - startTime
    response[WENDTIME_IDX] = endTime
    response[WSTATIME_IDX] = event[WSTATIME_IDX] if event[WSTATIME_IDX] > 0 else startTime
    priorCost = event[TSTACOST_IDX] if event[TSTACOST_IDX] > 0 else 0
    response[TSTACOST_IDX] = priorCost - (stampBegin-1000*time.time())


def inputHandler(event, response):
    startTime = 1000*time.time()
    number = randint(1,50)

    response[STATUS_IDX] = 200
    response[NUMBER_IDX] = number

    endTime = 1000*time.time()
    timestamp (event, response, startTime, endTime)


def divideby5Handler(event, response):
    startTime = 1000*time.time()
    input = event[NUMBER_IDX]
    output = input%5

    response[STATUS_IDX] = 200
    response[NUMBER_IDX] = output

    endTime = 1000*time.time()
    timestamp (event, response, startTime, endTime)


def incHandler(event, response):
    startTime = 1000*time.time()
    input = event[NUMBER_IDX]
    output = input+1

    response[STATUS_IDX] = 200
    response[NUMBER_IDX] = output

    endTime = 1000*time.time()
    timestamp (event, response, startTime, endTime)


def squareHandler(event, response):
    startTime = 1000*time.time()
    input = event[NUMBER_IDX]
    output = input*input

    response[STATUS_IDX] = 200
    response[NUMBER_IDX] = output

    endTime = 1000*time.time()
    timestamp (event, response, startTime, endTime)


def halfHandler(event, response):
    startTime = 1000*time.time()
    input = event[NUMBER_IDX]
    output = int(input/2)

    response[STATUS_IDX] = 200
    response[NUMBER_IDX] = output

    endTime = 1000*time.time()
    timestamp (event, response, startTime, endTime)


def doubleHandler(event, response):
    startTime = 1000*time.time()
    input = event[NUMBER_IDX]
    output = 2*input

    response[STATUS_IDX] = 200
    response[NUMBER_IDX] = output

    endTime = 1000*time.time()
    timestamp (event, response, startTime, endTime)


def divideby2Handler(event, response):
    startTime = 1000*time.time()
    input = event[NUMBER_IDX]
    output = input%2

    response[STATUS_IDX] = 200
    response[NUMBER_IDX] = output

    endTime = 1000*time.time()
    timestamp (event, response, startTime, endTime)


###############################################################################
###############################################################################


def inWorker(input_dict, output_arr):
    inputHandler(input_dict, output_arr)

def divideby5Worker(input_arr, output_arr):
    divideby5Handler(input_arr, output_arr) 

def incWorker(input_arr, output_arr):
    incHandler(input_arr, output_arr)

def squareWorker(input_arr, output_arr):
    squareHandler(input_arr, output_arr)

def halfWorker(input_arr, output_arr):
    halfHandler(input_arr, output_arr)

def doubleWorker(input_arr, output_arr):
    doubleHandler(input_arr, output_arr) 

def divideby2Worker(input_arr, output_arr):
    divideby2Handler(input_arr, output_arr) 


###############################################################################
###############################################################################


def main(event):
    ''' main function is our orchestrator!
    The first function of the workflow needs input and a shared arr to return
    response. Remaining functions need atleast 2 arguments, the response
    from previous function and a new one for it's own response. The response that
    returns from the last function is copied to an output dict and retured!
    '''
    output = {}
    ELEMENTS = 6
    event = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    input_arr = Array('d', ELEMENTS)
    input = Process(target=inWorker, args = (event, input_arr))
    input.start()
    input.join()

    divide5_arr = Array('d', ELEMENTS)
    divide5 = Process(target=divideby5Worker, args = (input_arr, divide5_arr))
    divide5.start()
    divide5.join()

    choices = {
        0: squareWorker,
        1: incWorker,
        2: divideby2Worker,
        3: doubleWorker,
        4: halfWorker
    }

    reminder     = divide5_arr[NUMBER_IDX]
    choiceWorker = choices[reminder]

    choice_arr = Array('d', ELEMENTS)
    choice = Process(target=choiceWorker, args = (input_arr, choice_arr))
    choice.start()
    choice.join()

    # Create a dict to return em!
    output['statusCode'] = choice_arr[STATUS_IDX]
    output['number'] = choice_arr[NUMBER_IDX]
    output['duration'] = choice_arr[DURATION_IDX]
    output['workflowStartTime'] = choice_arr[WSTATIME_IDX]
    output['workflowEndTime'] = choice_arr[WENDTIME_IDX]
    output['timeStampCost'] = choice_arr[TSTACOST_IDX]
    return output

if __name__=="__main__":
    print(main({}))
