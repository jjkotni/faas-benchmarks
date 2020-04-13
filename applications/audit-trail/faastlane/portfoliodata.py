import os
import json
import time

def timestamp(response, event, startTime, endTime, externalServicesTime):
    stampBegin = 1000*time.time()
    prior = event['duration'] if 'duration' in event else 0
    priorServiceTime = event['externalServicesTime'] if 'externalServicesTime' in event else 0
    response['duration']     = prior + endTime - startTime
    response['workflowEndTime'] = endTime
    response['workflowStartTime'] = event['workflowStartTime'] if 'workflowStartTime' in event else startTime
    priorCost = event['timeStampCost'] if 'timeStampCost' in event else 0
    response['externalServicesTime'] = priorServiceTime + externalServicesTime
    response['timeStampCost'] = priorCost - (stampBegin-1000*time.time())
    return response

def fetchPortfolioData(event):
    startTime = 1000*time.time()
    externalServicesTime = 0
    portfolio = event['body']['portfolio']
    portfolios = json.loads(open('data/portfolios.json', 'r').read())
    portfolioData = portfolios[portfolio]

    response = {'statusCode': 200,
                'body': {'portfolioData': portfolioData}}

    endTime = 1000*time.time()
    return timestamp(response, event, startTime, endTime, externalServicesTime)

# if __name__=="__main__":
#     event ={'body': {'portfolio': '1234'}}
#     print(fetchPortfolioData(event))
