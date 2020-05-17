import threading
from mpkmemalloc import *
import multiprocessing as mp

from marginBalance import main as marginbalanceFunction
from marketdata import main as marketDataFunction
from volume import main as volumeFunction
from trddate import main as trddateFunction
from lastpx import main as lastpxFunction
from side import main as sideFunction

PStateOut = []
marginOut = {}

def marginWorker():
    ######################################################
    global PStateOut
    #####################################################

    result = marginbalanceFunction(PStateOut)

    #####################################################
    global marginOut
    marginOut = result
    ######################################################

def marketProcessWrapper(event):
    global PStateOut
    response = marketDataFunction(event)
    PStateOut.append(response)

def volumeProcessWrapper(event):
    global PStateOut
    response = volumeFunction(event)
    PStateOut.append(response)

def trddateProcessWrapper(event):
    global PStateOut
    response = trddateFunction(event)
    PStateOut.append(response)

def sideProcessWrapper(event):
    global PStateOut
    response = sideFunction(event)
    PStateOut.append(response)

def lastpxProcessWrapper(event):
    global PStateOut
    response = lastpxFunction(event)
    PStateOut.append(response)

def PStateWorker(event):
    ######################################################
    global PStateOut
    PStateOut = []
    processes = []
    ######################################################

    for i in range(10):
    # for i in range(20):
        processes.append(threading.Thread(target=volumeProcessWrapper, args=[event]))
        processes.append(threading.Thread(target=trddateProcessWrapper, args=[event]))
        processes.append(threading.Thread(target=marketProcessWrapper, args=[event]))
        processes.append(threading.Thread(target=sideProcessWrapper, args=[event]))
        processes.append(threading.Thread(target=lastpxProcessWrapper, args=[event]))

    for process in processes:
        process.start()

    for process in processes:
        process.join()

def main(event):
    #All marked sections are overheads due to our system
    PState  = threading.Thread(target=PStateWorker, args=[event])
    margin  = threading.Thread(target=marginWorker)

    PState.start()
    PState.join()

    margin.start()
    margin.join()

    return marginOut

# if __name__ == "__main__":
#     print(main({'body': {'portfolioType':'S&P', 'portfolio':'1234'}}))
