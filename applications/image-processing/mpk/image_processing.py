from multiprocessing import Process
from PIL import Image, ImageFilter
from time import time
import threading as mt
from mpkmemalloc import *

TMP = "data/"

flip_result = {}
rotate_result = {}
filter_result = {}
gray_scale_result = {}
resize_result = {}

def flip(image_path, file_name, allocate_pkey):
    if allocate_pkey:
        tname = threading.currentThread().getName()
        pkey_thread_mapper(tname)
        tname = chr(ord(tname[0])+1)+tname[1:]

    with Image.open(image_path) as image:
        path_list = []
        path = TMP + "flip-left-right-" + file_name
        img = image.transpose(Image.FLIP_LEFT_RIGHT)
        img.save(path)
        path_list.append(path)

        path = TMP + "flip-top-bottom-" + file_name
        img = image.transpose(Image.FLIP_TOP_BOTTOM)
        img.save(path)
        path_list.append(path)

    global flip_result
    flip_result = {'result': path_list}

    if allocate_pkey:
        pymem_reset(tname)

def rotate(image_path, file_name, allocate_pkey):
    if allocate_pkey:
        tname = threading.currentThread().getName()
        pkey_thread_mapper(tname)
        tname = chr(ord(tname[0])+1)+tname[1:]

    with Image.open(image_path) as image:
        path_list = []
        path = TMP + "rotate-90-" + file_name
        img = image.transpose(Image.ROTATE_90)
        img.save(path)
        path_list.append(path)

        path = TMP + "rotate-180-" + file_name
        img = image.transpose(Image.ROTATE_180)
        img.save(path)
        path_list.append(path)

        path = TMP + "rotate-270-" + file_name
        img = image.transpose(Image.ROTATE_270)
        img.save(path)
        path_list.append(path)

    global rotate_result
    rotate_result = {'result': path_list}

    if allocate_pkey:
        pymem_reset(tname)

def filter(image_path, file_name, allocate_pkey):
    if allocate_pkey:
        tname = threading.currentThread().getName()
        pkey_thread_mapper(tname)
        tname = chr(ord(tname[0])+1)+tname[1:]

    with Image.open(image_path) as image:
        path_list = []
        path = TMP + "blur-" + file_name
        img = image.filter(ImageFilter.BLUR)
        img.save(path)
        path_list.append(path)

        path = TMP + "contour-" + file_name
        img = image.filter(ImageFilter.CONTOUR)
        img.save(path)
        path_list.append(path)

        path = TMP + "sharpen-" + file_name
        img = image.filter(ImageFilter.SHARPEN)
        img.save(path)
        path_list.append(path)

    global filter_result
    filter_result = {'result': path_list}

    if allocate_pkey:
        pymem_reset(tname)

def gray_scale(image_path, file_name, allocate_pkey):
    if allocate_pkey:
        tname = threading.currentThread().getName()
        pkey_thread_mapper(tname)
        tname = chr(ord(tname[0])+1)+tname[1:]

    with Image.open(image_path) as image:
        path = TMP + "gray-scale-" + file_name
        img = image.convert('L')
        img.save(path)

    global gray_scale_result
    gray_scale_result = {'result': [path]}

    if allocate_pkey:
        pymem_reset(tname)

def resize(image_path, file_name, allocate_pkey):
    if allocate_pkey:
        tname = threading.currentThread().getName()
        pkey_thread_mapper(tname)
        tname = chr(ord(tname[0])+1)+tname[1:]

    with Image.open(image_path) as image:
        path = TMP + "resized-" + file_name
        image.thumbnail((128, 128))
        image.save(path)

    global resize_result
    resize_result = {'result': [path]}

    if allocate_pkey:
        pymem_reset(tname)

def functionWorker(file_name, image_path, allocate_pkey):
    #All marked sections are overheads due to our system
    ######################################################
    pymem_setup_allocators(0)
    ######################################################
    path_list = []
    start = time()

    flip_thread       = mt.Thread(target=flip, args=[image_path, file_name, allocate_pkey], name="flip")
    rotate_thread     = mt.Thread(target=rotate, args=[image_path, file_name, allocate_pkey], name="rotate")
    filter_thread     = mt.Thread(target=filter, args=[image_path, file_name, allocate_pkey], name="filter")
    gray_scale_thread = mt.Thread(target=gray_scale, args=[image_path, file_name, allocate_pkey],name="gray_scale")
    resize_thread     = mt.Thread(target=resize, args=[image_path, file_name, allocate_pkey], name="resize")

    flip_thread.start()
    rotate_thread.start()
    filter_thread.start()
    gray_scale_thread.start()
    resize_thread.start()

    flip_thread.join()
    rotate_thread.join()
    filter_thread.join()
    gray_scale_thread.join()
    resize_thread.join()

    path_list += flip_result['result']
    path_list += rotate_result['result']
    path_list += filter_result['result']
    path_list += gray_scale_result['result']
    path_list += resize_result['result']

    ######################################################
    pymem_reset_pkru()
    ######################################################
    latency = time() - start
    print("No. images created: ", str(len(path_list)))
    return (latency, path_list)


def main(params):
    # OW will receive params here based on number of requests
    # We can have 16 versions of the same image for mp
    f_name = 'image.jpg'
    d_path = '{}{}'.format(TMP, f_name)

    workers = len (params) if (len(params) > 0) else 1

    threads = []
    for i in range(workers):
        t_name = 'worker' + str(i)
        threads.append (Process(target=functionWorker, args=[f_name,d_path,0], name=t_name))

    for idx, thread in enumerate(threads):
        thread.start ()
        thread.join ()

    result = {}
    for activation in params:
        result[activation] = 'Finished thread execution'

    return result

if __name__ == "__main__":
    out = main({'activation1':{}})
    # out = main({'activation1':{},'activation3':{},'activation4':{}, 'activation2': {},
    #          'activation31':{},'activation33':{},'activation34':{}, 'activation32': {},
    #          'activation45':{},'activation46':{},'activation47':{}, 'activation48': {}})
    print(out)
