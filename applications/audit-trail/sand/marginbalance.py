import time
def main(events):
    startTime = 1000*time.time()
    marketData = {}
    portfolioData = {}

    print(events)
    events = events['value']
    prevStartTimes = prevEndTimes = []
    for event in events:
        if 'startTime' in event:
            prevStartTimes.append(event['startTime'])
        if 'endTime' in event:
            prevEndTimes.append(event['endTime'])

        body = event['body']
        if 'marketData' in body:
            marketData = body['marketData']
        elif 'portfolioData' in body:
            portfolioData = body['portfolioData']

    securities = portfolioData['security']
    quantities = portfolioData['quantity']
    marginAccountBalance = portfolioData['marginBalance']

    portfolioMarketValue = 0
    for idx, security in enumerate(securities):
        portfolioMarketValue += quantities[idx]*marketData[security]

    #Maintenance Margin should be atleast 25% of market value for "long" securities
    #https://www.finra.org/rules-guidance/rulebooks/finra-rules/4210#the-rule
    result = False
    if marginAccountBalance >= 0.25*portfolioMarketValue:
        result = True

    response = {'statusCode': 200,
                'body': {'maintenaceMarginSatisfied': result}}

    priorWorkflowDuration = event['duration'] if 'duration' in event else 0
    #Obscure code, doing this to time.time() as late in the function as possible for end time
    response['duration'] = priorWorkflowDuration - (startTime-1000*time.time())
    return response
