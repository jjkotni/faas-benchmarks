import yfinance as yf
import time

def marketData(event):
    print("Start Time: ", str(1000*time.time()))
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

    print("End Time: ", str(1000*time.time()))
    return {'statusCode':200,
            'body': {'marketData':prices}}

# if __name__=="__main__":
#     event = {'body':{'portfolioType':'S&P'}}
#     print(marketData(event))
