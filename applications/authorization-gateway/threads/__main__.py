def divideby2Worker():
    ######################################################
    global inOut
    ######################################################

    result = divideby2Handler(inOut)

    ######################################################
    global divideOut
    divideOut = result
    ######################################################

def incWorker():
    ######################################################
    global divideOut
    ######################################################

    result = incHandler(divideOut)

    ######################################################
    global choiceOut
    choiceOut = result
    ######################################################

def doubleWorker():
    ######################################################
    global divideOut
    ######################################################

    result = doubleHandler(divideOut)

    ######################################################
    global choiceOut
    choiceOut = result
    ######################################################

def main(event):
    #All marked sections are overheads due to our system
    input     = threading.Thread(target=inWorker, args = [event])
    divideby2 = threading.Thread(target=divideby2Worker)

    input.start()
    input.join()

    divideby2.start()
    divideby2.join()

    choices = {
        0: incWorker,
        1: doubleWorker
