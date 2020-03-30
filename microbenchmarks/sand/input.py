#!/usr/bin/python
import json
from random import randint

def handle(event, context):
    number = randint(1,50)
    response = {
        "statusCode": 200,
        "body": {"number":number}
    }

    return response

