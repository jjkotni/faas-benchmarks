#!/usr/bin/python
import json

def handle(event, context):
    input = event['body']['number']
    output = input+1

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    return response