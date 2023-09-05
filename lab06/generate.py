# generates image of the sentence

import numpy as np
from PIL import Image, ImageFont, ImageDraw
from fontTools.ttLib import TTFont

symbols = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTÜVYZ"

sentence = 'EN GEVEZE KUŞ ÜMITTIR KALBIMIZDE HIÇ SUSMAZ'

font_size = 52
font_path = './arial.ttf'

def semitone(img):
    return (0.3 * img[:, :, 0] + 0.59 * img[:, :, 1] + 0.11 * img[:, :, 2]).astype(np.uint8)

def simple_bin(img: np.array, thres: int = 40):
    if len(img.shape) == 3 and img.shape[2] == 3:
        img = semitone(img)
    tmp = Image.fromarray(img)
    res_img = np.empty_like(img)
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            res_img[x, y] = 255 if img[x, y] > thres else 0
    return res_img

def calculate_profile(img: np.array, axis: int) -> np.array:
    return np.sum(img, axis=1 - axis)


def cut_white(img: np.array, profile: np.array, axis: int) -> np.array:
    start = profile.nonzero()[0][0]
    end = profile.nonzero()[0][-1] + 1

    if axis == 0:
        return img[start:end, :], profile[start:end]
    elif axis == 1:
        return img[:, start:end], profile[start:end]

def render_sentence(sentence: str):
    length = len(sentence)
    font = ImageFont.truetype(font_path, font_size)
    size = (font_size * length, font_size)
    image = Image.new(mode='RGB', size=size, color='white')
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), sentence, (0, 0, 0), font=font)

    tmp = np.array(image)
    tmp = simple_bin(tmp, 100)

    result = 255 - tmp

    for i in range(2):
        profile = calculate_profile(result, i)
        result, _ = cut_white(result, profile, i)


    return result


if __name__ == '__main__':

    array = render_sentence(sentence)
    inv = 255 - array
    img = Image.fromarray(array, 'L').convert('1')
    img.save(f'./images/inverted.bmp')
    img = Image.fromarray(inv, 'L').convert('1')
    img.save(f'./images/normal.bmp')
