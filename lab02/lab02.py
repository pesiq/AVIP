from PIL import Image
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
def binarization(image):
    pass

if __name__ == '__main__':

    imgn = 4

    with Image.open(f'./src/sample{imgn}.bmp').convert('RGB') as img:
        tmp1 = to_greyscale_balanced(img)
        tmp1.save(f'./out/grayscalebalanced{imgn}.bmp')
        tmp2 = to_grayscale_dumb(img)
        tmp2.save(f'./out/grayscaledumb{imgn}.bmp')

        binarization()