import boto3
import os
import json

BUCKET = os.environ['BUCKET']
FOLDER = os.environ['FOLDER']
PORTFOLIOS = os.environ['PORTFOLIOS']

def fetchPortfolioData(event, context):
    portfolio = event['body']['portfolio']

    response   = boto3.resource('s3').Object(BUCKET,os.path.join(FOLDER, PORTFOLIOS)).get()

    portfolios = json.loads(response['Body'].read().decode('utf-8'))

    portfolioData = portfolios[portfolio]

    return {'statusCode': 200,
            'body': {'portfolioData': portfolioData}}

# if __name__=="__main__":
#     event ={'body': {'portfolio': '1234'}}
#     print(fetchPortfolioData(event))
