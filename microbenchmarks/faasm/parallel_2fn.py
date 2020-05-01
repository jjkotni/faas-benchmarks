from pickle import loads, dumps
from time import time
from random import randint
from pyfaasm.core import get_state, get_state_size, set_state, chain_this_with_input, await_call

KEY_A = "dict_input"
KEY_B = "dict_square"
KEY_C = "dict_inc"
KEY_D = "dict_agg"

#### Utilities for functions needed to read, write and time shared memory #####

def get_dict_from_state(key):
    dict_size = get_state_size(key)
    pickled_dict = get_state(key, dict_size)
    return loads(pickled_dict)


def write_dict_to_state(key, dict_in):
    pickled_dict = dumps(dict_in)
    set_state(key, pickled_dict)


def timestamp (output, input, start, end):
    begin = 1000 * time ()
    prior = input.get ('duration', 0.0)
    output['duration'] = prior + end - start
    output['workflowEndTime'] = end
    output['workflowStartTime'] = input.get ('workflowStartTime', start)
    prior_cost = input.get ('timeStampCost', 0.0)
    output['timeStampCost'] = prior_cost - (begin - 1000 * time())
    return output


def agg_timestamp(response, events, start, end):
    begin = 1000*time()
    prior = 0
    p_cost = 0
    w_start = start
    for event in events:
        if 'duration' in event and event['duration'] > prior:
            prior = event['duration']
            #Pick timestamp costs from the same event/path
            p_cost = event['timeStampCost'] if 'timeStampCost' in event else 0
        if 'workflowStartTime' in event and event['workflowStartTime'] < w_start:
            w_start = event['workflowStartTime']

    response['duration']     = prior + end - start
    response['workflowEndTime'] = end
    response['workflowStartTime'] = w_start

    #Obscure code, doing to time.time() at the end of fn
    response['timeStampCost'] = p_cost - (begin-1000*time())
    return response

###############################################################################

def input_handler(input_bytes):
    start_time = 1000*time()
    number = randint(1,50)
    response = {
        "statusCode": 200,
        "body": {"number":number}
    }

    end_time = 1000*time()
    msg = timestamp(response, {}, start_time, end_time)
    write_dict_to_state(KEY_A, msg)


def square_handler(input_bytes):
    event = get_dict_from_state(KEY_A)
    start_time = 1000*time()
    input = event["body"]["number"]
    number = input * input
    response = {
        "statusCode": 200,
        "body": {"number":number}
    }

    end_time = 1000*time()
    msg = timestamp(response, event, start_time, end_time)
    write_dict_to_state(KEY_B, msg)


def inc_handler(input_bytes):
    event = get_dict_from_state(KEY_A)
    start_time = 1000*time()
    input = event["body"]["number"]
    number = input + 1
    response = {
        "statusCode": 200,
        "body": {"number":number}
    }

    end_time = 1000*time()
    msg = timestamp(response, event, start_time, end_time)
    write_dict_to_state(KEY_C, msg)


def agg_handler(input_bytes):
    events = []
    keys = [KEY_B, KEY_C]
    for key in keys:
        event = get_dict_from_state(key)
        events.append(event)

    start = 1000*time()
    aggregate = 0
    for event in events:
        aggregate += event['body']['number']
    response = {
        "statusCode": 200,
        "body":{"number":aggregate}
    }
    end = 1000*time()
    msg = agg_timestamp(response, events, start, end)
    write_dict_to_state(KEY_D, msg)

###############################################################################

# This is the main entrypoint
def faasm_main():
    # Write initial dictionary to state

    # Make the chained call, function 1
    input_id = chain_this_with_input(input_handler, b'')
    await_call(input_id)

    # chained parallel calls?
    square_id = chain_this_with_input(square_handler, b'')
    inc_id = chain_this_with_input(inc_handler, b'')

    await_call(square_id)
    await_call(inc_id)

    agg_id = chain_this_with_input(agg_handler, b'')
    await_call(agg_id)

    # Load from state again
    message = get_dict_from_state(KEY_D)

    # Check expectation
    print(message['workflowEndTime']-message['workflowStartTime']-message['timeStampCost']-message['duration'])
