import os
import json
import time

def fetchPortfolioData(event):
    startTime = 1000*time.time()
    portfolio = event['body']['portfolio']
    portfolios = json.loads(open('data/portfolios.json', 'r').read())
    portfolioData = portfolios[portfolio]

    response = {'statusCode': 200,
                'body': {'portfolioData': portfolioData}}

    priorWorkflowDuration = event['duration'] if 'duration' in event else 0
    #Obscure code, doing this to time.time() as late in the function as possible for end time
    response['duration'] = priorWorkflowDuration - (startTime-1000*time.time())
    return response

# if __name__=="__main__":
#     event ={'body': {'portfolio': '1234'}}
#     print(fetchPortfolioData(event))
