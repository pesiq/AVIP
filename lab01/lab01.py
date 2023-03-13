import math
from os import path
import numpy as np
from PIL import Image

def openImage(source: str) -> np.array:
        image = Image.open(source)
        return np.array(image)

def interpolate(image, factor: int):
    data = image.load()
    dim_original = image.size
    dim_resulting = tuple(d * factor for d in dim_original)
    result = Image.new('RGB', dim_resulting)
    new_data = result.load()


    for x in range(image.size[0]):
        for y in range(image.size[1]):
            for offsetx in range(factor):
                for offsety in range(factor):
                    new_data[x * factor + offsetx, y * factor + offsety] = data[x, y]
    return result

def decimate(image, factor: int):
    data = image.load()

    dim_original = image.size
    dim_resulting = tuple(math.floor(d / factor) for d in dim_original)

    result = Image.new('RGB', dim_resulting)
    new_data = result.load()

    for x in range(result.size[0]):
        for y in range(result.size[1]):
            new_data[x, y] = data[x * factor, y * factor]
    return result

def twoPassResampling(image, ifactor: int, dfactor: int):
    return decimate(interpolate(image, ifactor), dfactor)

def onePassResampling(image, ifactor: int, dfactor: int):
    dim_original = image.size
    dim_resulting = tuple(int(d * ifactor/dfactor) - 1 for d in dim_original)

    result = Image.new('RGB', dim_resulting)

    data = image.load()
    new_data = result.load()

    for x in range(result.size[0]):
        for y in range(result.size[1]):
            new_data[x, y] = data[math.floor(x * dfactor / ifactor), math.floor(y * dfactor / ifactor)]
    return result



if __name__ == '__main__':
    srcpath = ''
    resultpath = ''

    imgn = 2

    img = Image.open(f'./srcimg/sample{imgn}.png').convert('RGB')


    interpolate(img, 2).save(f'./resultimg/sample1{imgn}.png')

    decimate(img, 2).save(f'./resultimg/sample2{imgn}.png')

    twoPassResampling(img, 4, 7).save(f'./resultimg/sample3{imgn}.png')

    onePassResampling(img, 4, 7).save(f'./resultimg/sample4{imgn}.png')
