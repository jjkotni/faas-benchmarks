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


def aggTimestamp(events, response, startTime, endTime):
    stampBegin = 1000*time.time()
    prior = 0
    priorCost = 0
    workflowStartTime = startTime
    for event in events:
        if event[DURATION_IDX] > 0 and event[DURATION_IDX] > prior:
            prior = event[DURATION_IDX]
            #Pick timestamp costs from the same event/path
            priorCost = event[TSTACOST_IDX] if event[TSTACOST_IDX] > 0 else 0
        if event[WSTATIME_IDX] > 0 and event[WSTATIME_IDX] < workflowStartTime:
            workflowStartTime = event[WSTATIME_IDX]

    response[DURATION_IDX] = prior + endTime - startTime
    response[WENDTIME_IDX] = endTime
    response[WSTATIME_IDX] = workflowStartTime

    #Obscure code, doing to time.time() at the end of fn
    response[TSTACOST_IDX] = priorCost - (stampBegin-1000*time.time())
    return response


def inputHandler(event, response):
    startTime = 1000*time.time()
    number = randint(1,50)

    response[STATUS_IDX] = 200
    response[NUMBER_IDX] = number

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


def reminderHandler(event, response):
    startTime = 1000*time.time()
    input = event[NUMBER_IDX]
    output = input%2

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


def aggHandler(events, response):
    startTime = 1000*time.time()
    aggregate = 0
    durations = []

    for event in events:
        if event[DURATION_IDX] > 0:
            durations.append(event[DURATION_IDX])
        aggregate += event[NUMBER_IDX]

    response[STATUS_IDX] = 200
    response[NUMBER_IDX] = aggregate

    endTime = 1000*time.time()
    aggTimestamp (events, response, startTime, endTime)


###############################################################################
###############################################################################


def inWorker(input_dict, output_arr):
    inputHandler(input_dict, output_arr)

def incWorker(input_arr, output_arr):
    incHandler(input_arr, output_arr)

def squareWorker(input_arr, output_arr):
    squareHandler(input_arr, output_arr)

def halfWorker(input_arr, output_arr):
    halfHandler(input_arr, output_arr)

def remWorker(input_arr, output_arr):
    reminderHandler(input_arr, output_arr)

def doubleWorker(input_arr, output_arr):
    doubleHandler(input_arr, output_arr)

def aggWorker(inc_arr, square_arr, rem_arr, half_arr, double_arr, agg_arr):
    aggHandler([inc_arr, square_arr, rem_arr, half_arr, double_arr], agg_arr)


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
    #All marked sections are overheads due to our system
    input_arr = Array('d', ELEMENTS)
    input = Process(target=inWorker, args=(event, input_arr))
    inc_arr   = Array('d', ELEMENTS)
    increment = Process(target=incWorker, args=(input_arr, inc_arr))
    sq_arr = Array('d', ELEMENTS)
    square = Process(target=squareWorker, args=(input_arr, sq_arr))
    half_arr = Array('d', ELEMENTS)
    half = Process(target=halfWorker, args=(input_arr, half_arr))
    rem_arr = Array('d', ELEMENTS)
    reminder  = Process(target=remWorker, args=(input_arr, rem_arr))
    double_arr = Array('d', ELEMENTS)
    double = Process(target=doubleWorker, args=(input_arr, double_arr))
    agg_arr = Array('d', ELEMENTS)
    aggregate = Process(target=aggWorker, args=(inc_arr, sq_arr, \
        rem_arr, half_arr, double_arr, agg_arr))

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

    # Create a dict to return em!
    output['statusCode'] = agg_arr[STATUS_IDX]
    output['number'] = agg_arr[NUMBER_IDX]
    output['duration'] = agg_arr[DURATION_IDX]
    output['workflowStartTime'] = agg_arr[WSTATIME_IDX]
    output['workflowEndTime'] = agg_arr[WENDTIME_IDX]
    output['timeStampCost'] = agg_arr[TSTACOST_IDX]
    return output

if __name__=="__main__":
    output = main({})
    mtime = output['workflowEndTime']-output['workflowStartTime']-output['timeStampCost']-output['duration']
    print("Interaction Time: {}".format(mtime))
