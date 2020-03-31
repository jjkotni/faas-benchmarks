import jwt
import time

def generateToken(event, context):
    user = event['body']['user']

    #Use the same secret in the decoder to authorize a client
    secret = 'faas-iisc'

    payload = {'issuedAt': time.time(),
               'expiresAt': time.time() + 30*86400,
               'effect': 'allow',
               'issuer': 'generateToken.generateToken',
               'username': user
              }

    token = jwt.encode(payload, secret, algorithm='HS256')

    return {'statusCode': 200,
            'body': {'authorizationToken': token}}

# if __name__=="__main__":
#     print(generateToken({'body':{'user':'guest'}}))
