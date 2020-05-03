from pickle import loads, dumps
from time import time
from random import randint
from pyfaasm.core import get_state, get_state_size, set_state, chain_this_with_input, await_call

KEY_A = "dict_input"
KEY_B = "dict_square"
KEY_C = "dict_inc"
KEY_D = "dict_half"
KEY_E = "dict_divide"

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
    event = get_dict_from_state(KEY_B)
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


def half_handler(input_bytes):
    event = get_dict_from_state(KEY_C)
    start_time = 1000*time()
    input = event["body"]["number"]
    number = input / 2
    response = {
        "statusCode": 200,
        "body": {"number":number}
    }

    end_time = 1000*time()
    msg = timestamp(response, event, start_time, end_time)
    write_dict_to_state(KEY_D, msg)


def divide_by2_handler(input_bytes):
    event = get_dict_from_state(KEY_D)
    start_time = 1000*time()
    input = event["body"]["number"]
    number = input % 2
    response = {
        "statusCode": 200,
        "body": {"number":number}
    }

    end_time = 1000*time()
    msg = timestamp(response, event, start_time, end_time)
    write_dict_to_state(KEY_E, msg)

###############################################################################

# This is the main entrypoint
def faasm_main():
    # Write initial dictionary to state

    # Make the chained call, function 1
    input_id = chain_this_with_input(input_handler, b'')
    await_call(input_id)

    # chained call, function 2
    square_id = chain_this_with_input(square_handler, b'')
    await_call(square_id)

    # chained call, function 2
    inc_id = chain_this_with_input(inc_handler, b'')
    await_call(inc_id)

    # chained call, function 2
    half_id = chain_this_with_input(half_handler, b'')
    await_call(half_id)

    # chained call, function 2
    div_id = chain_this_with_input(divide_by2_handler, b'')
    await_call(div_id)

    # Load from state again
    message = get_dict_from_state(KEY_E)

    # Check expectation
    print(message['workflowEndTime']-message['workflowStartTime']-message['timeStampCost']-message['duration'])