import json
import time
import ast
import gc
import nltk
from nltk.tokenize import word_tokenize
from util import *

def main(event):
    startTime = 1000*time.time()
    tokens = word_tokenize(event['body']['message'])
    response = {'statusCode': 200, "body":len(tokens)}
    endTime = 1000*time.time()
    return timestamp(response, event, startTime, endTime, 0)
