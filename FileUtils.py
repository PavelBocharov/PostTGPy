import glob
import os
import uuid

import numpy
from PIL import Image


def get_list_images(root_dir: str):
    dirs = glob.glob(pathname=root_dir + "/**", recursive=True)
    imgs = []
    for dir in dirs:
        low_dir = dir.lower()
        if (low_dir.endswith(".jpg")
                | low_dir.endswith(".jpeg")
                | low_dir.endswith(".png")
                | low_dir.endswith(".bmp")):
            imgs.append(dir)
    return imgs


def add_watermark(temp_save_dir: str, image_path: str, watermark_path: str):
    """ Document """
    new_name = temp_save_dir + "/" + str(uuid.uuid4()) + get_file_type(image_path)
    # load watermark
    wm = Image.open(watermark_path)
    wm_x, wm_y = wm.size
    # load image
    img = Image.open(image_path)
    img_x, img_y = img.size

    new_img = img.copy()
    new_img.paste(wm, (img_x - wm_x, img_y - wm_y), wm)

    save_array = numpy.asarray(new_img)
    Image.fromarray(save_array).save(new_name)
    return new_name


def get_file_type(file: str):
    root, extension = os.path.splitext(file)
    return extension
