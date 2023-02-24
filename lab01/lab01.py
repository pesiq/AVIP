from os import path
import numpy as np
from PIL import Image

def openImage(source: str) -> np.array:
        image = Image.open(source).convert('RGB')
        return np.array(image)

def interpolate(image):
    pass

def decimate(image):
    pass

def twoPassResampling(image):
    pass

def onePassResampling(image):
    pass



if __name__ == '__main__':
    pass