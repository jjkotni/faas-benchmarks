from PIL import Image, ImageFilter
from time import time
import threading as mt

TMP = "data/"


def flip(image, file_name):
    path_list = []
    path = TMP + "flip-left-right-" + file_name
    img = image.transpose(Image.FLIP_LEFT_RIGHT)
    img.save(path)
    path_list.append(path)

    path = TMP + "flip-top-bottom-" + file_name
    img = image.transpose(Image.FLIP_TOP_BOTTOM)
    img.save(path)
    path_list.append(path)

    return path_list


def rotate(image, file_name):
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

    return path_list


def filter(image, file_name):
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

    return path_list


def gray_scale(image, file_name):
    path = TMP + "gray-scale-" + file_name
    img = image.convert('L')
    img.save(path)
    return [path]


def resize(image, file_name):
    path = TMP + "resized-" + file_name
    image.thumbnail((128, 128))
    image.save(path)
    return [path]


def functionWorker(file_name, image_path, allocate_pkey):
    path_list = []
    start = time()
    with Image.open(image_path) as image:
        tmp = image
        path_list += flip(image, file_name)
        path_list += rotate(image, file_name)
        path_list += filter(image, file_name)
        path_list += gray_scale(image, file_name)
        path_list += resize(image, file_name)

    latency = time() - start
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
        threads.append (mt.Thread(target=functionWorker, args=[f_name,d_path,0], name=t_name))

    for idx, thread in enumerate(threads):
        thread.start()
        thread.join()

    result = {}
    for activation in params:
        result[activation] = 'Finished thread execution'

    # The images are uploaded to s3 client here, we don't need them!
    return result

if __name__ == "__main__":
    out = main({'activation1':{},'activation3':{},'activation4':{}, 'activation2': {},
             'activation31':{},'activation33':{},'activation34':{}, 'activation32': {},
             'activation45':{},'activation46':{},'activation47':{}, 'activation48': {}})
    print(out)
