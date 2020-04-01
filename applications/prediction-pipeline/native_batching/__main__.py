import os
import threading
import multiprocessing as mp

from predict import predictHandler
from resize import resizeHandler
from render import renderHandler

resizeOut  = {}
predictOut = {}
renderOut  = {}

def resizeWorker(event):
    result = resizeHandler(event)

    ######################################################
    global resizeOut
    resizeOut = result
    ######################################################

def predictWorker():
    ######################################################
    global resizeOut
    ######################################################

    result = predictHandler(resizeOut)

    ######################################################
    global predictOut
    predictOut = result
    ######################################################

def renderWorker():
    ######################################################
    global predictOut
    ######################################################

    result = renderHandler(predictOut)

    ######################################################
    global renderOut
    renderOut = result
    ######################################################

def functionWorker(event):
    resize  = threading.Thread(target=resizeWorker, args=[event])
    predict = threading.Thread(target=predictWorker)
    render  = threading.Thread(target=renderWorker)

    resize.start()
    resize.join()

    predict.start()
    predict.join()

    render.start()
    render.join()

    return renderOut

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

# if __name__ == '__main__':
#     out = main({'activation1':{},'activation3':{},'activation4':{}, 'activation2': {},
#              'activation31':{},'activation33':{},'activation34':{}, 'activation32': {},
#              'activation45':{},'activation46':{},'activation47':{}, 'activation48': {}})
