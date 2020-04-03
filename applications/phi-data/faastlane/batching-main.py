import os
import threading
import json
import multiprocessing as mp
from mpkmemalloc import *

from identifyphi import identifyphiHandler
from anonymize import anonymizeHandler
from deidentify import deidentifyHandler

identifyphiOut = {}
choiceOut = {}

def identifyphiWorker(event):
    ######################################################
    tname = threading.currentThread().getName()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    ######################################################

    result = identifyphiHandler(event)

    ######################################################
    global identifyphiOut
    identifyphiOut = result
    pymem_reset(tname)
    ######################################################

def deidentifyWorker():
    ######################################################
    tname = threading.currentThread().getName()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    global identifyphiOut
    ######################################################

    result = deidentifyHandler(identifyphiOut)

    ######################################################
    global choiceOut
    choiceOut = result
    pymem_reset(tname)
    ######################################################

def anonymizeWorker():
    ######################################################
    tname = threading.currentThread().getName()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    global identifyphiOut
    ######################################################

    result = anonymizeHandler(identifyphiOut)

    ######################################################
    global choiceOut
    choiceOut = result
    pymem_reset(tname)
    ######################################################

def functionWorker(event):
    identifyphi = threading.Thread(target=identifyphiWorker,
                                   args = [event])
    identifyphi.start()
    identifyphi.join()

    choices = {
        'anonymize' : anonymizeWorker,
        'deidentify': deidentifyWorker
    }

    usage        = identifyphiOut['body']['usage']
    choiceWorker = choices.get(usage)
    choice       = threading.Thread(target=choiceWorker)

    choice.start()
    choice.join()

    return choiceOut

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
        processes.append(mp.Process(target=processWrapper,
                                    args=[activationId, event, responseQueue]))

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    result = {}
    for x in range(len(events)):
        result.update(responseQueue.get())

    return(result)

# if __name__=="__main__":
#     event = json.loads(open("phi.json").read())
#     print(main(event))
