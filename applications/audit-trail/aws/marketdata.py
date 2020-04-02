import yfinance as yf

def marketData(event, context):
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

    return {'statusCode':200,
            'body': {'marketData':prices}}

if __name__=="__main__":
    event = {'body':{'portfolioType':'S&P'}}
    print(marketData(event))
