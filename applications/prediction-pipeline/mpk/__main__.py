import os
import time
import threading
from mpkmemalloc import *
from util import *

from predict import predictHandler
from resize import resizeHandler
from render import renderHandler

resizeOut  = {}
predictOut = {}
renderOut  = {}

def resizeWorker(event):
    ######################################################
    pkey_thread_mapper()
    ######################################################

    result = resizeHandler(event)

    ######################################################
    global resizeOut
    pymem_allocate_from_shmem()
    resizeOut = copy_output(result)
    pymem_reset()
    ######################################################

def predictWorker():
    ######################################################
    pkey_thread_mapper()
    global resizeOut
    ######################################################

    result = predictHandler(resizeOut)

    ######################################################
    global predictOut
    pymem_allocate_from_shmem()
    predictOut = copy_output(result)
    predictOut['memsetTime'] += clear_output(resizeOut['body'])
    pymem_reset()
    ######################################################

def renderWorker():
    ######################################################
    pkey_thread_mapper()
    global predictOut
    ######################################################

    result = renderHandler(predictOut)

    ######################################################
    global renderOut
    pymem_allocate_from_shmem()
    renderOut = copy_output(result)
    pymem_reset()
    ######################################################

def main(event):
    #All marked sections are overheads due to our system
    ######################################################
    pymem_setup_allocators(0)
    ######################################################

    resize  = threading.Thread(target=resizeWorker, args=[event])
    predict = threading.Thread(target=predictWorker)
    render  = threading.Thread(target=renderWorker)

    resize.start()
    resize.join()

    predict.start()
    predict.join()

    render.start()
    render.join()

    ######################################################
    pymem_reset_pkru()
    ######################################################
    return renderOut

# if __name__ == "__main__":
#     out = main({})
#     out['functionInteractions'] = out['workflowEndTime'] - out['workflowStartTime'] - out['duration'] - out['timeStampCost']
#     print(out)
