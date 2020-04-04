import os
import json
import time

def fetchPortfolioData(event):
    print("Start Time: ", str(1000*time.time()))
    portfolio = event['body']['portfolio']
    portfolios = json.loads(open('data/portfolios.json', 'r').read())
    portfolioData = portfolios[portfolio]

    print("End Time: ", str(1000*time.time()))
    return {'statusCode': 200,
            'body': {'portfolioData': portfolioData}}

# if __name__=="__main__":
#     event ={'body': {'portfolio': '1234'}}
#     print(fetchPortfolioData(event))
