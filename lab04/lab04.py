import numpy as np
from PIL import Image
import math

def binarization(img, border):
    if len(img.shape) == 3 and img.shape[2] == 3:
        img = to_semi_tone(img)
    return np.fromiter(map(
                lambda pixel: 255 if pixel > border else 0,
                img.flatten()
            ), dtype=np.uint8).reshape(img.shape)

def grayscale (image):
    data = image.load()

    result = Image.new('L', image.size)

    new_data = result.load()

    for x in range(image.size[0]):
        for y in range(image.size[1]):
            new_data[x, y] = round(0.3 * data[x,y][0] + 0.59 * data[x,y][1] + 0.11 * data[x,y][2])
    return result

operators = {
    'x': np.array(
        [[1, 1, 1],
         [0, 0, 0],
         [-1, -1, -1]]
    ),
    'y': np.array(
        [[1, 0, -1],
         [1, 0, -1],
         [1, 1, -1]]
    )
}

def get_frame(img: np.array, x: int, y: int) -> np.array:
    return img[x - 3 // 2:x + 3 // 2 + 1,
               y - 3 // 2:y + 3 // 2 + 1]

def apply_operator(frame: np.array, direction):
    frame = frame.astype(np.int32)
    if direction == 'x':
        return np.sum(operators['x'] * frame)
    elif direction == 'y':
        return np.sum(operators['y'] * frame)
    elif direction == 'g' or direction == 'b':
        return np.sqrt(np.sum(operators['x'] * frame) ** 2 + np.sum(operators['y'] * frame) ** 2)
    else:
        raise ValueError("Unsupported direction")
            


def grads(img, direction):
    new_img = np.zeros_like(img, dtype=np.float64)
    x, y = 1, 1
    while x < img.shape[0] - 1:
        if x % 2 == 0:
            while y + 1 < img.shape[1] - 1:
                frame = get_frame(img, x, y)
                new_img[x, y] = apply_operator(frame, direction)
                y += 1
        else:
            while y - 1 > 1:
                frame = get_frame(img, x, y)
                new_img[x, y] = apply_operator(frame, direction)
                y -= 1
        x += 1
    new_img = new_img / np.max(new_img) * 255
    if direction == 'b':
        return binarization(new_img, 64)
    elif direction == 'x' or direction == 'y' or direction == 'g':
        return new_img.astype(np.uint8)
    else:
        raise ValueError("Unsupported direction")


def outline(img):
    gx = grads(img, 'x')
    gy = grads(img, 'y')
    g = grads(img, 'g')
    b = grads(img, 'b')

    return (gx, gy, g, b)


if __name__ == "__main__":

    n = 1

    srcpath = f'./src/sample{n}.bmp'
    outpath = f'./out/result{n}'

    with Image.open(srcpath).convert('L') as img:
        tmp = np.array(img)

        res = outline(tmp)

        Image.fromarray(res[0]).save(f'{outpath}_x.bmp')
        Image.fromarray(res[1]).save(f'{outpath}_y.bmp')
        Image.fromarray(res[2]).save(f'{outpath}_g.bmp')
        Image.fromarray(res[3]).save(f'{outpath}_b.bmp')



