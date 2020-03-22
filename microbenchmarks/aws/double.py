import json

def doubleHandler(event, context):
    input = event['body']['number']
    output = 2*input

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    return response

# if __name__ == "__main__":
#     response = squareHandler({"body":{"number":2}}, {})
#     print(response)
