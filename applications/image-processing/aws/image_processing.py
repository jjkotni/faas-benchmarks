from PIL import Image, ImageFilter
from time import time
import threading as mt

TMP = "data/"

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

def rotate(image):
    path_list = []
    imgName = "rotate-90-" + IMAGE
    img = image.transpose(Image.ROTATE_90)
    img.save(os.path.join(FILE_DIR,imgName))
    path_list.append(imgName)

    imgName = "rotate-180-" + IMAGE
    img = image.transpose(Image.ROTATE_180)
    img.save(os.path.join(FILE_DIR,imgName))
    path_list.append(imgName)

    imgName = "rotate-270-" + IMAGE
    img = image.transpose(Image.ROTATE_270)
    img.save(os.path.join(FILE_DIR,imgName))
    path_list.append(imgName)

    return path_list


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


def gray_scale(image):
    imgName = "gray-scale-" + IMAGE
    img = image.convert('L')
    img.save(os.path.join(FILE_DIR,imgName))
    return [imgName]


def resize(image):
    imgName = "resized-" + IMAGE
    image.thumbnail((128, 128))
    image.save(os.path.join(FILE_DIR,imgName))
    return [imgName]


def functionWorker(file_name, image_path, allocate_pkey):
    path_list = []
    start = time()
    with Image.open(image_path) as image:
        tmp = image
        path_list += flip(image)
        path_list += rotate(image)
        path_list += filter(image)
        path_list += gray_scale(image)
        path_list += resize(image)

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

#if __name__ == "__main__":
#    out = main({'activation1':{},'activation3':{},'activation4':{}, 'activation2': {},
#             'activation31':{},'activation33':{},'activation34':{}, 'activation32': {},
#             'activation45':{},'activation46':{},'activation47':{}, 'activation48': {}})
#    print(out)
