import boto3
import os
import json

BUCKET     = 'faas-iisc'
FOLDER     = 'audit-trail'
PORTFOLIOS = 'portfolios.json'

def main(event):
    portfolio = event['body']['portfolio']

    s3 = boto3.client('s3', aws_access_key_id="AKIAJW2FQCBYG7JUWGPQ",
                      aws_secret_access_key="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",
                      region_name="us-east-1")

    portfolios_string = s3.get_object(Bucket = BUCKET, Key = os.path.join(FOLDER, PORTFOLIOS))['Body'].read()
    portfolios = json.loads(portfolios_string.decode('utf-8'))

    portfolioData = portfolios[portfolio]

    return {'statusCode': 200,
            'body': {'portfolioData': portfolioData}}

# if __name__=="__main__":
#     event ={'body': {'portfolio': '1234'}}
#     print(fetchPortfolioData(event))
