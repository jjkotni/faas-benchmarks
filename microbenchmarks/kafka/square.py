from time import time
from random import randint
from util import *
import sys

def handler(event, out_topics=None):
    start_time = 1000*time()
    input = event["body"]["number"]
    number = input * input
    response = {
        "statusCode": 200,
        "body": {"number":number}
    }

    end_time = 1000*time()
    message = timestamp(response, event, start_time, end_time)
    if out_topics:
        send (out_topics[0], message)
    else:
        print(message)

'''This function can be used for choice, 2 sequence where it is 
a terminating function, else in 5 sequence as a bridge. If it
receives 2 arguments, it's bridge else terminating.
'''
if __name__ == "__main__":
    out_topic = None
    in_topic = sys.argv[1]
    if (len (sys.argv) > 2):
        out_topic = sys.argv[2]

    consumer = get_consumer (in_topic)
    if out_topic:
        forward (handler, consumer, [out_topic])
    else:
        receive (handler, consumer)
    # clear the stuff!
    consumer.unsubscribe()
