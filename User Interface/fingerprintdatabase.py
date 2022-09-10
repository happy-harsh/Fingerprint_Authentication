from importlib.resources import path
from PIL import Image
import cv2 as cv
import shutil
# img_PIL = Image.open(r'C:\Program Files\Mantra\MFS100\Driver\MFS100Test\FingerData')
# img_PIL.show()

import os


def biometric_captr():
    path = r"C:/Program Files/Mantra/MFS100/Driver/MFS100Test/FingerData/FingerImage.bmp"
    assert os.path.isfile(path)
    with open(path, "r") as f:
        pass
    shutil.copy(f, "Firebase database folder")
    # img_PIL = Image.open(path)
    # img_PIL.show()
