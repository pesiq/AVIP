from PIL import Image
import numpy as np
import math

def to_greyscale_balanced (image):
    data = image.load()

    result = Image.new('L', image.size)

    new_data = result.load()

    for x in range(image.size[0]):
        for y in range(image.size[1]):
            new_data[x, y] = round(0.3 * data[x,y][0] + 0.59 * data[x,y][1] + 0.11 * data[x,y][2])
    return result

def to_grayscale_dumb(image):
    data = image.load()

    result = Image.new('L', image.size)

    new_data = result.load()

    for x in range(image.size[0]):
        for y in range(image.size[1]):
            new_data[x, y] = round(data[x,y][0] + data[x,y][1] + data[x,y][2] / 3)
    return result

def threshold(image):
    bins = np.arange(image.min() - 1, image.max() + 1)
    hist, base = np.histogram(image, bins=bins, density=True)
    base = base[1:].astype(np.uint8)

    w0_raw = np.cumsum(hist)
    w1_raw = np.ones(shape=w0_raw.shape) - w0_raw
    t_rank = 0
    i_max = 0
    for i, (w0, w1) in enumerate(zip(w0_raw, w1_raw)):
        m0 = np.sum(base[:i] * hist[:i] / w0)
        m1 = np.sum(base[i + 1:] * hist[i + 1:] / w1)
        d0 = np.sum(hist[:i] * (base[:i] - m0)**2)
        d1 = np.sum(hist[i + 1:] * (base[i + 1:] - m1)**2)
        d_all = w0 * d0 + w1 * d1
        d_class = w0 * w1 * (m0 - m1)**2
        if d_all == 0:
            i_max = i
            break
        if d_class / d_all > t_rank:
            t_rank = d_class / d_all
            i_max = i

    return base[i_max]
def findMean(data, threshold):
    data_ft = data.flatten()
    data_1 = data_ft[data_ft >= threshold]
    data_2 = data_ft[data_ft < threshold]
    mean_1 = data_1.mean() if data_1.size > 0 else 0
    mean_2 = data_2.mean() if data_2.size > 0 else 0
    return mean_1, mean_2


def Helper(x, y, inner, outer, old_image, new_image, diff):
    s_window = old_image[y:min(y + inner, old_image.shape[0]), x:min(x + inner, old_image.shape[1])]
    l_window = old_image[max(y - outer // 2 + 1, 0):min(y + outer // 2 + inner - 1, old_image.shape[0]),
               max(x - outer // 2 + 1, 0):min(x + outer // 2 + inner - 1, old_image.shape[1])]

    t = threshold(l_window)
    m1, m2 = findMean(l_window, t)

    if abs(m1 - m2) >= diff:
        new_image[y:min(y + inner, old_image.shape[0]),
                  x:min(x + inner, old_image.shape[1])][s_window > t] = 255
    else:
        center = s_window[s_window.shape[0] // 2, s_window.shape[1] // 2]
        if abs(m1 - center) < abs(m2 - center):
            new_image[y:min(y + inner, old_image.shape[0]),
                      x:min(x + inner, old_image.shape[1])] = 255


def Eikvel_binarization(old_image, diff, inner, outer):
    new_image = np.zeros(shape=old_image.shape)

    x, y = 0, 0
    while y + inner <= old_image.shape[0]:
        if y % 2 == 0:
            while x + inner < old_image.shape[1]:
                Helper(x, y, inner, outer, old_image, new_image, diff)
                x += inner
        else:
            while x - inner > 0:
                Helper(x, y, inner, outer, old_image, new_image, diff)
                x -= inner

        y += inner

    return new_image.astype(np.uint8)




if __name__ == '__main__':


    # for imgn in range(1, 5):
    #     with Image.open(f'./src/sample{imgn}.bmp').convert('RGB') as img:
    #         print(f'Opened image #{imgn}')
    #         tmp1 = to_greyscale_balanced(img)
    #         tmp1.save(f'./out/grayscale{imgn}.bmp')
    #         print(f'Image #{imgn} grayscale done')
    #         print(f'Starting binarizing')
    #         tmp2 = Image.fromarray(Eikvel_binarization(np.array(tmp1), 5, 3, 15), 'L')
    #         tmp2.save(f'./out/binary{imgn}.bmp')
    #         print(f'Image #{imgn} done')
    imgn = 5

    with Image.open(f'./src/sample{imgn}.bmp').convert('RGB') as img:
        print(f'Opened image #{imgn}')
        tmp1 = to_greyscale_balanced(img)
        tmp1.save(f'./out/grayscale{imgn}.bmp')
        print(f'Image #{imgn} grayscale done')
        print(f'Starting binarizing')
        tmp2 = Image.fromarray(Eikvel_binarization(np.array(tmp1), 5, 3, 15), 'L')
        tmp2.save(f'./out/binary{imgn}.bmp')
        print(f'Image #{imgn} done')