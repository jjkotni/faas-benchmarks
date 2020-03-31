import os
import threading

from marginBalance import checkMarginAccountBalance
from marketdata import marketData
from portfoliodata import fetchPortfolioData

marketOut    = {}
portfolioOut = {}
marginOut    = {}

def marginWorker():
    global marketOut, portfolioOut
    data = [marketOut, portfolioOut]

    print(data)
    result = checkMarginAccountBalance(data)

    global marginOut
    marginOut = result

def marketWorker(event):
    result = marketData(event)

    global marketOut
    marketOut = result

def portfolioWorker(event):
    result = fetchPortfolioData(event)

    global portfolioOut
    portfolioOut = result

def main(event):
    portfolio  = threading.Thread(target=portfolioWorker, args=[event])
    market     = threading.Thread(target=marketWorker,    args=[event])
    margin     = threading.Thread(target=marginWorker)

    market.start()
    portfolio.start()

    market.join()
    portfolio.join()

    margin.start()
    margin.join()

    return marginOut

# if __name__ == "__main__":
#     print(main({'body': {'portfolioType':'S&P', 'portfolio':'1234'}}))
