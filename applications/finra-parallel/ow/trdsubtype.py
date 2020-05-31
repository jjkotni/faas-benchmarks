import json
import time
from util import *

def main(event):
    startTime = 1000*time.time()

    portfolio = event['body']['portfolio']
    portfolios = json.loads(open('data/portfolios.json', 'r').read())
    data = portfolios[portfolio]

    valid = True

    for trade in data:
        subtype = trade['TrdSubType']
        # Tag ID: 829, Tag Name: TrdSubType, Valid values: 0,1
        if not (subtype == 1 or subtype == 0):
            valid = False
            break

    response = {'statusCode': 200, 'body': {'valid':valid, 'portfolio': portfolio}}
    endTime = 1000*time.time()
    return timestamp(response, event,startTime, endTime, 0)

# if __name__=="__main__":
#     print(main({"body": {"portfolioType": "S&P","portfolio": "1234"}}))
