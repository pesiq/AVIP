import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
from generate import symbols


def get_profiles(img):
    return {
        'x': {
            'y': np.sum(img, axis=0),
            'x': np.arange(
                start=1, stop=img.shape[1] + 1).astype(int)
        },
        'y': {
            'y': np.arange(
                start=1, stop=img.shape[0] + 1).astype(int),
            'x': np.sum(img, axis=1)
        }
    }


def write_profile(img, letter, type='x'):
    profiles = get_profiles(img)

    if type == 'x':
        plt.bar(x=profiles['x']['x'], height=profiles['x']['y'], width=0.9)

        # plt.ylim(0, 52)

    elif type == 'y':
        plt.barh(y=profiles['y']['y'], width=profiles['y']['x'], height=0.9)

        # plt.ylim(52, 0)

    else:
        raise Exception('Unsupported profile')

    # plt.xlim(0, 55)

    plt.savefig(f'results/profiles/{type}/{letter}.png')
    plt.clf()


if __name__ == '__main__':
    method_prefix = 'Image_Profiles'

    for letter in symbols:
        img_src = Image.open(f'./letters/{letter}.bmp').convert('L')
        img_src_arr = np.array(img_src)

        img_src_arr[img_src_arr == 0] = 1
        img_src_arr[img_src_arr == 255] = 0

        write_profile(img_src_arr, letter, type='x')
        write_profile(img_src_arr, letter, type='y')