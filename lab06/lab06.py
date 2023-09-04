import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from PIL.ImageOps import invert


def calculate_profile(img: np.array, axis: int) -> np.array:
    return np.sum(img, axis=1 - axis)


def cut_black(img: np.array, profile: np.array, axis: int) -> np.array:
    start = profile.nonzero()[0][0]
    end = profile.nonzero()[0][-1] + 1

    if axis == 0:
        return img[start:end, :], profile[start:end]
    elif axis == 1:
        return img[:, start:end], profile[start:end]


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
                letter_borders.append(i + 1)

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
    with Image.open(f'./images/normal.bmp') as image:

        img = np.array(image)

        profile_x = calculate_profile(img, 0)
        profile_y = calculate_profile(img, 1)
        bins_x = np.arange(start=1, stop=img.shape[0] + 1).astype(int)
        bins_y = np.arange(start=1, stop=img.shape[1] + 1).astype(int)

        bar(profile_x / 255, bins_x, 0)
        plt.savefig(f'./results/profile_x.png')
        plt.clf()

        bar(profile_y / 255, bins_y, 1)
        plt.savefig(f'./results/profile_y.png')
        plt.clf()

        img_letters, letter_borders = split_letters(img, profile_y)
        print(letter_borders)

        # result_img = Image.fromarray(img, 'L')
        result = Image.new("RGB", image.size)
        result.paste(image)
        draw = ImageDraw.Draw(result)

        for border in letter_borders:
            draw.line((border, 0, border, img.shape[1]), fill='green')

        result.save(f"results/result.png")
