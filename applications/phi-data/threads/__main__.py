import threading
import json
from util import *

from identifyphi import main as identifyphiHandler
from anonymize import main as anonymizeHandler
from deidentify import main as deidentifyHandler
from analytics import main as analyticsHandler

identifyphiOut = {}
choiceOut = {}
anonymizeOut = {}

def identifyphiWorker(event):
    result = identifyphiHandler(event)

    ######################################################
    global identifyphiOut
    identifyphiOut = result
    ######################################################

def deidentifyWorker():
    ######################################################
    global identifyphiOut
    ######################################################

    result = deidentifyHandler(identifyphiOut)

    ######################################################
    global choiceOut
    choiceOut = result
    ######################################################

def anonymizeWorker():
    ######################################################
    global identifyphiOut
    ######################################################

    result = anonymizeHandler(identifyphiOut)

    ######################################################
    global anonymizeOut
    anonymizeOut = result
    ######################################################

def analyticsWorker():
    ######################################################
    global anonymizeOut
    ######################################################

    result = analyticsHandler(anonymizeOut)

    ######################################################
    global choiceOut
    choiceOut = result
    ######################################################

def main(event):
    identifyphi = threading.Thread(target=identifyphiWorker, args = [event])
    analytics = threading.Thread(target=analyticsWorker)

    identifyphi.start()
    identifyphi.join()

    choices = {
        0 : anonymizeWorker,
        1 : deidentifyWorker
    }

    usage        = identifyphiOut['body']['usage']
    choiceWorker = choices.get(usage)

    choice    = threading.Thread(target=choiceWorker)

    choice.start()
    choice.join()

    if usage == 0:
        analytics.start()
        analytics.join()

    return choiceOut

# if __name__=="__main__":
#     event = json.loads(open("phi.json").read())
#     out = main(event)
#     out['functionInteractions'] = out['workflowEndTime'] - out['workflowStartTime'] - out['duration'] - out['timeStampCost']
#     print(out)
#     gc.disable()
