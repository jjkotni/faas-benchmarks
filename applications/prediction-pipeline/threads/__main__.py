import os
import threading

from predict import predictHandler
from resize import resizeHandler
from render import renderHandler

resizeOut  = {}
predictOut = {}
renderOut  = {}

def resizeWorker(event):
    result = resizeHandler(event)

    global resizeOut
    resizeOut = result

def predictWorker():
    global resizeOut

    result = predictHandler(resizeOut)

    global predictOut
    predictOut = result

def renderWorker():
    global predictOut

    result = renderHandler(predictOut)

    global renderOut
    renderOut = result

def main(event):
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

if __name__ == "__main__":
    main({})
