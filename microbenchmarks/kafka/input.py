from time import time
from random import randint
from util import *
import sys

def handler(event):
    start_time = 1000*time()
    number = randint(1,50)
    response = {
        "statusCode": 200,
        "body": {"number":number}
    }

    end_time = 1000*time()
    return timestamp(response, event, start_time, end_time)


if __name__ == "__main__":
    out_topic = sys.argv[1]
    output = handler({})
    send (out_topic, output)
