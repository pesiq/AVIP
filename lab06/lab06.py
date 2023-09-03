import numpy as np
import matplotlib.pyplot as plt
from os import path
from helpers import calculate_profile, image_to_np_array, cut_black
from PIL import Image, ImageDraw
from PIL.ImageOps import invert

def split_letters(img: np.array, profile: np.array):
    assert img.shape[1] == profile.shape[0]
    letters = []
    letter_borders = []
    letter_start = 0
    is_empty = True

    for i in range(img.shape[1]):
        if profile[i] == 0:
            if not is_empty:
                is_empty = True
                letters.append(img[:, letter_start:i + 1])
                letter_borders.append(i+1)

        else:
            if is_empty:
                is_empty = False
                letter_start = i
                letter_borders.append(letter_start)

    letters.append(img[:, letter_start:img.shape[1] - 1])

    return letters, letter_borders


def bar(data, bins, axis):
    if axis == 1:
        plt.bar(x=bins, height=data)

    elif axis == 0:
        plt.barh(y=bins, width=data)

    else:
        raise ValueError('Invalid axis')

if __name__ == '__main__':
    img = image_to_np_array('sentence_white.bmp')

    profile_x = calculate_profile(img, 0)
    profile_y = calculate_profile(img, 1)
    bins_x = np.arange(start=1, stop=img.shape[0] + 1).astype(int)
    bins_y = np.arange(start=1, stop=img.shape[1] + 1).astype(int)

    bar(profile_x / 255, bins_x, 0)
    plt.savefig(path.join('results', f'profile_x.png'))
    plt.clf()

    bar(profile_y / 255, bins_y, 1)
    plt.savefig(path.join('results', f'profile_y.png'))
    plt.clf()

    img_letters, letter_borders = split_letters(img, profile_y)
    print(letter_borders)

    result_img = Image.fromarray(img.astype(np.uint8), 'L')
    rgb_img = Image.new("RGB", result_img.size)
    rgb_img.paste(result_img)
    draw = ImageDraw.Draw(rgb_img)
    
    for border in letter_borders:
        draw.line((border, 0, border, img.shape[1]), fill='green')

    rgb_img.save(f"results/result.png")

    for i, letter in enumerate(img_letters):
        for axis in (0, 1):
            # letter_profile = calculate_profile(letter, axis)
            # letter, _ = cut_black(letter, letter_profile, axis)
            letter_img = Image.fromarray(letter.astype(np.uint8), 'L').convert('1')

            letter_img.save(f"results/symbols_inversed/letter_{i}.png")

        letter_img = invert(letter_img)
        letter_img.save(f"results/symbols/letter_{i}.png")
