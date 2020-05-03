import json
import time
import ast
import gc
import nltk
from nltk.tokenize import word_tokenize
from mpkmemalloc import *
from util import *

def main(event):
    startTime = 1000*time.time()
    externalServicesTime = 0
    tokens = word_tokenize(event['body']['message'])
    pymem_allocate_from_shmem()
    response = {'statusCode': 200, "body":len(tokens)}
    endTime = 1000*time.time()
    return timestamp(response, event, startTime, endTime, externalServicesTime)
