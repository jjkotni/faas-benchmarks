#!/usr/bin/python
import json

def handle(event, context):
    input = event['body']['number']
    output = int(input/2)

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    return response

# if __name__ == "__main__":
#     response = squareHandler({"body":{"number":3}}, {})
#     print(response)
