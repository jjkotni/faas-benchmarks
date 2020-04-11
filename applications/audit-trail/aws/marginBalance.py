import time
def timestamp(response, events, startTime, endTime):
    stampBegin = 1000*time.time()
    prior = 0
    priorCost = 0
    workflowStartTime = startTime
    for event in events:
        if 'duration' in event and event['duration'] > prior:
            prior = event['duration']
            #Pick timestamp costs from the same event/path
            priorCost = event['timeStampCost'] if 'timeStampCost' in event else 0
        if 'workflowStartTime' in event and event['workflowStartTime'] < workflowStartTime:
            workflowStartTime = event['workflowStartTime']

    response['duration']     = prior + endTime - startTime
    response['workflowEndTime'] = endTime
    response['workflowStartTime'] = workflowStartTime

    #Obscure code, doing to time.time() at the end of fn
    response['timeStampCost'] = priorCost - (stampBegin-1000*time.time())
    return response

def checkMarginAccountBalance(events, context):
    startTime = 1000*time.time()
    marketData = {}
    portfolioData = {}

    for event in events:
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

    endTime = 1000*time.time()
    return timestamp(response, events, startTime, endTime)
