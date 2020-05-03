from time import time
from util import *
from multiprocessing import Process
import sys


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
        if 'workflowstart' in event and event['workflowstart'] < w_start:
            w_start = event['workflowstart']

    response['duration']     = prior + end - start
    response['workflowEndTime'] = end
    response['workflowstart'] = w_start

    #Obscure code, doing to time.time() at the end of fn
    response['timeStampCost'] = p_cost - (begin-1000*time())
    return response


def handler(events):
    start = 1000*time()
    aggregate = 0
    durations = []
    for event in events:
        if 'duration' in event:
            durations.append(event['duration'])
        aggregate += event['body']['number']

    response = {
        "statusCode": 200,
        "body":{"number":aggregate}
    }

    end = 1000*time()
    print(agg_timestamp(response, events, start, end))


def wait (consumer, topics):
    response = []
    merged_topics = topics
    for message in consumer:
        response.append(message.value)
        merged_topics -= 1

        if merged_topics == 0:
            break

    return response


'''This function takes 2 arguments number of producers
and input topic
'''
if __name__ == "__main__":
    producers = int(sys.argv[1])
    in_topic = sys.argv[2]

    consumer = get_consumer (in_topic)
    merge = wait (consumer, producers)
    proc = Process (target=handler, args=(merge,))
    proc.start ()
    proc.join ()
    # clear the stuff!
    consumer.unsubscribe()
