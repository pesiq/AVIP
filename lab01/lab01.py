from os import path
import numpy as np
from PIL import Image

def openImage(source: str) -> np.array:
        image = Image.open(source).convert('RGB')
        return np.array(image)

def interpolate(image: np.array, factor: int):
    dim_original = image.shape[0:2]
    dim_resulting = tuple(d * 2 for d in dim_original)

    result = np.empty((*dim_resulting, 3))


    for x in range(dim_resulting[0]):
        for y in range(dim_resulting[1]):
            result[x, y] = image[min(int(round(x / factor)), dim_original[0] - 1), min(int(round(y / factor)), dim_original[1] - 1)]
    return result

def decimate(image: np.array, factor: int):
    dim_original = image.shape[0:2]
    dim_resulting = tuple(int(d / 2) for d in dim_original)

    result = np.empty((*dim_resulting, 3))

    for x in range(dim_resulting[0]):
        for y in range(dim_resulting[1]):
            result[x, y] = image[
                min(int(round(x * factor)), dim_original[0] - 1), min(int(round(y * factor)), dim_original[1] - 1)]
    return result

def twoPassResampling(image: np.array, ifactor: int, dfactor: int):
    temp = interpolate(image, ifactor)
    return decimate(temp, dfactor)

def onePassResampling(image: np.array, factor: float):
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
    imgn = 2
    img = openImage(f'./srcimg/sample{imgn}.png')
    new_img = interpolate(img, 2)
    res = Image.fromarray(new_img.astype(np.uint8), 'RGB')
    res.save(f'./resultimg/sample{imgn}.png')

    imgn = 1
    img = openImage(f'./srcimg/sample{imgn}.png')
    new_img = decimate(img, 2)
    res = Image.fromarray(new_img.astype(np.uint8), 'RGB')
    res.save(f'./resultimg/sample{imgn}.png')

    imgn = 1
    img = openImage(f'./srcimg/sample{imgn}.png')
    new_img = onePassResampling(img, 1.4)
    res = Image.fromarray(new_img.astype(np.uint8), 'RGB')
    res.save(f'./resultimg/sample{3}.png')

    imgn = 2
    img = openImage(f'./srcimg/sample{imgn}.png')
    new_img = twoPassResampling(img, 4, 7)
    res = Image.fromarray(new_img.astype(np.uint8), 'RGB')
    res.save(f'./resultimg/sample{4}.png')