import json

def main(args):
    events = args['value']
    aggregate = 0
    for event in events:
        aggregate += event['body']['number']

    response = {
        "statusCode": 200,
        "body":{"number":aggregate}
    }

    return response
