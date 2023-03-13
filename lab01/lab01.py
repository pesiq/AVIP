from os import path
import numpy as np
from PIL import Image

def openImage(source: str) -> np.array:
        image = Image.open(source)
        return np.array(image)

def interpolate(image, factor: int):
    data = image.load()
    dim_original = image.size
    dim_resulting = tuple(d * 2 for d in dim_original)
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
    dim_resulting = tuple(int(d / 2) for d in dim_original)

    result = Image.new('RGB', dim_resulting)
    new_data = result.load()

    for x in range(result.size[0]):
        for y in range(result.size[1]):
            new_data[x, y] = data[x * factor, y * factor]
    return result

def twoPassResampling(image, ifactor: int, dfactor: int):
    return decimate(interpolate(image, ifactor), dfactor)

def onePassResampling(image: np.array, factor: float) -> np.array:
    dim_original = image.shape[0:2]
    dim_resulting = tuple(int(d * 2) for d in dim_original)

    result = np.empty((*dim_resulting, 3))

    for x in range(dim_resulting[0]):
        for y in range(dim_resulting[1]):
            result[x, y] = image[
                min(int(round(x / factor)), dim_original[0] - 1),
                min(int(round(y / factor)), dim_original[1] - 1)
            ]
    return result



if __name__ == '__main__':
    srcpath = ''
    resultpath = ''

    img = Image.open(f'./srcimg/sample1.png').convert('RGB')
    interpolate(img, 2).save(f'./resultimg/sample1.png')

    img = Image.open(f'./srcimg/sample1.png').convert('RGB')
    decimate(img, 2).save(f'./resultimg/sample2.png')


    # img = openImage(f'./srcimg/sample{imgn}.png')
    # new_img = onePassResampling(img, 1.4)
    # res = Image.fromarray(new_img.astype(np.uint8), 'RGB')
    # res.save(f'./resultimg/sample{3}.png')
    #
    # imgn = 2
    # img = openImage(f'./srcimg/sample{imgn}.png')
    # new_img = twoPassResampling(img, 4, 7)
    # res = Image.fromarray(new_img.astype(np.uint8), 'RGB')
    # res.save(f'./resultimg/sample{4}.png')