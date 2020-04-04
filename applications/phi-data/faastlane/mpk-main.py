import os
import threading
import json
from mpkmemalloc import *

from identifyphi import main as identifyphiHandler
from anonymize import main as anonymizeHandler
from deidentify import main as deidentifyHandler

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

def main(event):
    #All marked sections are overheads due to our system
    ######################################################
    pymem_setup_allocators(0)
    ######################################################
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
    ######################################################
    pymem_reset_pkru()
    ######################################################
    return choiceOut

# if __name__=="__main__":
#     event = json.loads(open("phi.json").read())
#     print(main(event))
