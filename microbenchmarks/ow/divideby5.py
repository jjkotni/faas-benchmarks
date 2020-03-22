import json

def divideby5Handler(event):
    input = event['body']['number']
    output = input%5

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    return response

# if __name__ == "__main__":
#     response = squareHandler({"body":{"number":2}}, {})
#     print(response)
