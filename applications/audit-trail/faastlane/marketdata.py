import yfinance as yf
import time

def marketData(event):
    startTime = 1000*time.time()
    portfolioType = event['body']['portfolioType']

    tickersForPortfolioTypes = {'S&P': ['GOOG', 'AMZN', 'MSFT']}
    tickers = tickersForPortfolioTypes[portfolioType]

    prices = {}
    for ticker in tickers:
        tickerObj = yf.Ticker(ticker)
        #Get last closing price
        data = tickerObj.history(period="1")
        price = data['Close'].unique()[0]
        prices[ticker] = price

    response = {'statusCode':200,
                'body': {'marketData':prices}}

    priorWorkflowDuration = event['duration'] if 'duration' in event else 0
    #Obscure code, doing this to time.time() as late in the function as possible for end time
    response['duration'] = priorWorkflowDuration - (startTime-1000*time.time())
    return response

# if __name__=="__main__":
#     event = {'body':{'portfolioType':'S&P'}}
#     print(marketData(event))
