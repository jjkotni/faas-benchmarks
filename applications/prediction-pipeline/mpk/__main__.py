import os
import threading
from mpkmemalloc import *

from predict import predictHandler
from resize import resizeHandler
from render import renderHandler

resizeOut  = {}
predictOut = {}
renderOut  = {}

def resizeWorker(event):
    ######################################################
    tname = threading.currentthread().getname()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    ######################################################

    result = resizeHandler(event)

    ######################################################
    global resizeOut
    resizeOut = result
    pymem_reset(tname)
    ######################################################

def predictWorker():
    ######################################################
    tname = threading.currentthread().getname()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    global resizeOut
    ######################################################

    result = predictHandler(resizeOut)

    ######################################################
    global predictOut
    predictOut = result
    pymem_reset(tname)
    ######################################################

def renderWorker():
    ######################################################
    tname = threading.currentthread().getname()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    global predictOut
    ######################################################

    result = renderHandler(predictOut)

    ######################################################
    global renderOut
    renderOut = result
    pymem_reset(tname)
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
#     main({})
