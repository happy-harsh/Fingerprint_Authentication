from importlib.resources import path
from PIL import Image
# img_PIL = Image.open(r'C:\Program Files\Mantra\MFS100\Driver\MFS100Test\FingerData')
# img_PIL.show()

import os


def biometric_captr():
    path = r"C:/Program Files/Mantra/MFS100/Driver/MFS100Test/FingerData/FingerImage.bmp"
    assert os.path.isfile(path)
    with open(path, "r") as f:
        pass
    return path
    img_PIL = Image.open(path)
    img_PIL.show()
