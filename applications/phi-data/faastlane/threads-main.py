import os
import threading
import json
import base64
import logging
import uuid
import hashlib
import logging
import boto3

from identifyphi import main as identifyphiHandler
from anonymize import main as anonymizeHandler
from deidentify import main as deidentifyHandler

identifyphiOut = {}
choiceOut = {}

def identifyphiWorker(event):
    result = identifyphiHandler(event)

    global identifyphiOut
    identifyphiOut = result

def deidentifyWorker():
    global identifyphiOut
    result = deidentifyHandler(identifyphiOut)

    global choiceOut
    choiceOut = result

def anonymizeWorker():
    global identifyphiOut
    result = anonymizeHandler(identifyphiOut)

    global choiceOut
    choiceOut = result

def main(event):
    identifyphi = threading.Thread(target=identifyphiWorker, args = [event])

    identifyphi.start()
    identifyphi.join()

    choices = {
        'anonymize' : anonymizeWorker,
        'deidentify': deidentifyWorker
    }

    usage        = identifyphiOut['body']['usage']
    choiceWorker = choices.get(usage)

    choice    = threading.Thread(target=choiceWorker)

    choice.start()
    choice.join()

    return choiceOut

# if __name__=="__main__":
#     event = json.loads(open("phi.json").read())
#     print(main(event))
