import os
import threading
import multiprocessing as mp

from marginBalance import checkMarginAccountBalance
from marketdata import marketData
from portfoliodata import fetchPortfolioData

marketOut    = {}
portfolioOut = {}
marginOut    = {}

def marginWorker():
    ######################################################
    global marketOut, portfolioOut
    data = [marketOut, portfolioOut]
    ######################################################

    result = checkMarginAccountBalance(data)

    ######################################################
    global marginOut
    marginOut = result
    ######################################################

def marketWorker(event):
    result = marketData(event)

    ######################################################
    global marketOut
    marketOut = result
    ######################################################

def portfolioWorker(event):
    result = fetchPortfolioData(event)

    ######################################################
    global portfolioOut
    portfolioOut = result
    ######################################################

def functionWorker(event):
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

def processWrapper(activationId, event, responseQueue):
    response = functionWorker(event)

    ######################################################
    responseQueue.put({activationId:response})
    ######################################################

def main(events):
    processes = []
    responseQueue = mp.Queue()

    for activationId, event in events.items():
        processes.append(mp.Process(target=processWrapper, args=[activationId, event, responseQueue]))

    for idx, process in enumerate(processes):
        process.start()

    for idx, process in enumerate(processes):
        process.join()

    result = {}
    for x in range(len(events)):
        result.update(responseQueue.get())

    return(result)

# if __name__ == "__main__":
#     print(main({'activation1':{'body': {'portfolioType':'S&P', 'portfolio':'1234'}}}))
