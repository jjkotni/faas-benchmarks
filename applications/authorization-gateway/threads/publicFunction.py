import jwt
import threading
from datetime import date

def generatePolicy(user, effect, resource):
    authResponse = {}

    policyDocument = {}
    policyDocument['Version'] = "2012-10-17"
    policyDocument['Statement'] = []
    statement = {}
    statement['Action'] = ['execute-api:Invoke']
    statement['Effect'] = effect
    statement['Resource'] = [resource]
    policyDocument['Statement'].append(statement)
    authResponse['policyDocument'] = policyDocument

    authResponse['principalId'] = user
    return authResponse

def authorize(event, context):
    if 'Authorization' in event:
        token = event['Authorization']
    elif 'headers' in event:
        token = event['headers']['Authorization']
    else:
        token = event['authorizationToken']

    resource = "arn:aws:execute-api:us-east-1:767037556445:uzagvfg5u7/*/POST/privateFunc"

    secret = 'faas-iisc'
    authorizationPayload = jwt.decode(token, secret, algorithm = 'HS256')
    if 'username' in authorizationPayload and 'effect' in authorizationPayload:
        return generatePolicy(authorizationPayload['username'], authorizationPayload['effect'],resource)
    else:
        raise Exception('Unauthorized')

def privateFunction(event, context):
    print('Entered private function successfully!')
    return {'statusCode': 200}

def main(event, context):
    authorization = threading.Thread(target=authorize, args = [event, context])
    function = threading.Thread(target=privateFunction, args = [event, context])

    authorization.start()
    authorization.join()

    function.start()
    function.join()

    return {'statusCode': 200}

# if __name__=="__main__":
#     event = {'statusCode': 200,  'headers' : {'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3N1ZWRBdCI6MTU4NTU3Njg0OS4xOTA0OTE3LCJleHBpcmVzQXQiOjE1ODgxNjg4NDkuMTkwNDkyLCJlZmZlY3QiOiJhbGxvdyIsImlzc3VlciI6ImdlbmVyYXRlVG9rZW4uZ2VuZXJhdGVUb2tlbiIsInVzZXJuYW1lIjoiZ3Vlc3QifQ.XFZyDpemSOyGlkibwqLnK-CNrSsD30hPEz6Cmiovycg'}}
#     print(main(event,{}))
