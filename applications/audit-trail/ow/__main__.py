import yfinance as yf
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

def main(event):
    startTime = 1000*time.time()
    externalServicesTime = 0
    portfolioType = event['body']['portfolioType']

    tickersForPortfolioTypes = {'S&P': ['GOOG', 'AMZN', 'MSFT']}
    tickers = tickersForPortfolioTypes[portfolioType]

    prices = {}
    for ticker in tickers:
        tickerObj = yf.Ticker(ticker)
        #Get last closing price
        tickTime = 1000*time.time()
        data = tickerObj.history(period="1")
        externalServicesTime += 1000*time.time() - tickTime
        price = data['Close'].unique()[0]
        prices[ticker] = price

    response = {'statusCode':200,
                'body': {'marketData':prices}}

    endTime = 1000*time.time()
    return timestamp(response, event, startTime, endTime, externalServicesTime)

# if __name__=="__main__":
#     event = {'body':{'portfolioType':'S&P'}}
#     print(marketData(event))
