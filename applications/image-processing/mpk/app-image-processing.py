import threading
import time
from random import randint
from mpkmemalloc import *
import os
import json
import base64
import boto3

inOut     = {}
incOut    = {}
squareOut = {}
halfOut   = {}
remOut    = {}
aggOut    = {}
doubleOut = {}


FILE_DIR = '/tmp'
BUCKET = os.environ['BUCKET']
FOLDER = os.environ['FOLDER']
IMAGE  = os.environ['IMAGE']

def fetchHandler(event):
    boto3.Session(
        ).resource('s3'
        ).Bucket(BUCKET
        ).download_file(
            os.path.join(FOLDER,   IMAGE),
            os.path.join(FILE_DIR, IMAGE))

    img = open(os.path.join(FILE_DIR, IMAGE), 'rb')
    img_encode = base64.b64encode(img.read()).decode("utf-8")

    response = {
        "statusCode": 200,
        "body": {"image": img_encode}
    }

    return response

def filter(image):
    path_list = []
    imgName = "blur-" + IMAGE
    img = image.filter(ImageFilter.BLUR)
    img.save(os.path.join(FILE_DIR,imgName))
    path_list.append(imgName)

    imgName = "contour-" + IMAGE
    img = image.filter(ImageFilter.CONTOUR)
    img.save(os.path.join(FILE_DIR,imgName))
    path_list.append(imgName)

    imgName = "sharpen-" + IMAGE
    img = image.filter(ImageFilter.SHARPEN)
    img.save(os.path.join(FILE_DIR,imgName))
    path_list.append(imgName)

    return path_list

def flip(image):
    path_list = []
    imgName = "flip-left-right-" + IMAGE
    img = image.transpose(Image.FLIP_LEFT_RIGHT)
    img.save(os.path.join(FILE_DIR,imgName))
    path_list.append(imgName)

    imgName = "flip-top-bottom-" + IMAGE
    img = image.transpose(Image.FLIP_TOP_BOTTOM)
    img.save(os.path.join(FILE_DIR,imgName))
    path_list.append(imgName)

    return path_list

def getImage(body):
    imageString = base64.decodestring(body['image'].encode("utf-8"))
    imageFile = open(os.path.join(FILE_DIR, IMAGE), "wb")
    imageFile.write(imageString)
    imageFile.close()
    image = Image.open(os.path.join(FILE_DIR, IMAGE))
    return image

def imageProcessingHandler(processingFn, event):
    image  = getImage(event['body'])
    images = processingFn(image)

    processed = []
    for modImage in images:
        boto3.client('s3').upload_file(os.path.join(FILE_DIR, modImage),
                                       BUCKET,
                                       os.path.join(FOLDER,   modImage))

        processed.append(modImage)

    response = {
        "statusCode": 200,
        "body": {"processedImages": processed}
    }

    return response

def filterHandler(event):
    return imageProcessingHandler(filter, event)

def flipHandler(event):
    return imageProcessingHandler(flip, event)

def squareHandler(event):
    input = event['body']['number']
    output = input*input

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    return response

def halfHandler(event):
    input = event['body']['number']
    output = int(input/2)

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    return response

def reminderHandler(event):
    input = event['body']['number']
    output = input%2

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    return response

def doubleHandler(event):
    input = event['body']['number']
    output = 2*input

    response = {
        "statusCode": 200,
        "body": {"number":output}
    }

    return response

def aggregateHandler(events):
    aggregate = 0
    for event in events:
        aggregate += len(event['body']['processedImages'])

    response = {
        "statusCode": 200,
        "body":{"numProcessedImages":aggregate}
    }

    return response

def fetchWorker(event):
    ######################################################
    tname = threading.currentThread().getName()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    ######################################################

    result = fetchHandler(event)

    ######################################################
    global inOut
    inOut = result
    pymem_reset(tname)
    ######################################################

def filterWorker():
    ######################################################
    tname = threading.currentThread().getName()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    global inOut
    ######################################################

    result = filterHandler(inOut)

    ######################################################
    global incOut
    incOut = result
    pymem_reset(tname)
    ######################################################

def flipWorker():
    ######################################################
    tname = threading.currentThread().getName()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    global inOut
    ######################################################

    result = flipHandler(inOut)

    ######################################################
    global squareOut
    squareOut = result
    pymem_reset(tname)
    ######################################################

def halfWorker():
    ######################################################
    tname = threading.currentThread().getName()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    global inOut
    ######################################################

    result = halfHandler(inOut)

    ######################################################
    global halfOut
    halfOut = result
    pymem_reset(tname)
    ######################################################

def remWorker():
    ######################################################
    tname = threading.currentThread().getName()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    global inOut
    ######################################################

    result = reminderHandler(inOut)

    ######################################################
    global remOut
    remOut = result
    pymem_reset(tname)
    ######################################################

def doubleWorker():
    ######################################################
    tname = threading.currentThread().getName()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    global inOut
    ######################################################

    result = doubleHandler(inOut)

    ######################################################
    global doubleOut
    doubleOut = result
    pymem_reset(tname)
    ######################################################

def aggregateWorker():
    ######################################################
    tname = threading.currentThread().getName()
    pkey_thread_mapper(tname)
    tname = chr(ord(tname[0])+1)+tname[1:]
    global incOut, squareOut, remOut, halfOut, doubleOut
    ######################################################

    result = aggregateHandler([incOut, squareOut,
                            remOut, halfOut, doubleOut])

    ######################################################
    global aggOut
    aggOut = result
    pymem_reset(tname)
    ######################################################

def main(event):
    #All marked sections are overheads due to our system
    ######################################################
    pymem_setup_allocators(0)
    ######################################################

    input     = threading.Thread(target=fetchWorker, args = [event])
    increment = threading.Thread(target=filterWorker)
    square    = threading.Thread(target=flipWorker)
    # half      = threading.Thread(target=halfWorker)
    # reminder  = threading.Thread(target=remWorker)
    # double    = threading.Thread(target=doubleWorker)
    aggregate = threading.Thread(target=aggregateWorker)

    input.start()
    input.join()

    #Parallel Functions
    increment.start()
    square.start()
    # half.start()
    # reminder.start()
    # double.start()

#     reminder.join()
#     half.join()
    square.join()
    increment.join()
    # double.join()

    aggregate.start()
    aggregate.join()

    ######################################################
    pymem_reset_pkru()
    ######################################################
    return aggOut

# if __name__=="__main__":
#     main()
