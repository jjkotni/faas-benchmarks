def main(events):
    marketData = {}
    portfolioData = {}

    for event in events['value']:
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

    return {'statusCode': 200,
            'body': {'maintenaceMarginSatisfied': result}}
