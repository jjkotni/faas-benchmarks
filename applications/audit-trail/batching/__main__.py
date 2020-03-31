import os
import threading
from mpkmemalloc import *

from marginBalance import checkMarginAccountBalance
from marketdata import marketData
from portfoliodata import fetchPortfolioData

marketOut    = {}
portfolioOut = {}
marginOut    = {}

def marginWorker():
    ######################################################
    tname = threading.currentthread().getname()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    global marketOut, portfolioOut
    data = [marketOut, portfolioOut]
    ######################################################

    result = checkMarginAccountBalance(data)

    ######################################################
    global marginOut
    marginOut = result
    pymem_reset(tname)
    ######################################################

def marketWorker(event):
    ######################################################
    tname = threading.currentthread().getname()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    ######################################################

    result = marketData(event)

    ######################################################
    global marketOut
    marketOut = result
    pymem_reset(tname)
    ######################################################

def portfolioWorker(event):
    ######################################################
    tname = threading.currentthread().getname()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    ######################################################

    result = fetchPortfolioData(event)

    ######################################################
    global portfolioOut
    portfolioOut = result
    pymem_reset(tname)
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
    #All marked sections are overheads due to our system
    ######################################################
    pymem_setup_allocators(0)
    ######################################################

    response = functionWorker(event)

    ######################################################
    responseQueue.put({activationId:response})
    pymem_reset_pkru()
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
