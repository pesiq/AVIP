import numpy as np
from PIL import Image
import math

def simple_binarization(img, threshold):
    result = Image.new('1', image.size)

    image = result.load()

    for x in range(image.size[0] - 3):
        for y in range(image.size[1] - 3):
            if img[x][y] > threshold:
                image[x, y] = 1
            else:
                image[x, y] = 0
    return result





def get_frame(img, x, y):
    aperture = 3
    frame = np.zeros_like(aperture, aperture)
    for x_offset in range(aperture):
        for y_offset in range(aperture):
            result = [x_offset][y_offset] = int(img[x + x_offset, y + y_offset])

    return result

def grad_matrix(img):
    Gx = np.array(
        [
            [-1, -1, -1],
            [0, 0, 0],
            [1, 1, 1]
         ]
        )
    Gy = np.rot90(Gx)

    size_x = img.size[0] - 2
    size_y = img.size[1] - 2

    x_matrix = np.zeros_like((size_x, size_y), dtype = int)
    y_matrix = np.zeros_like((size_x, size_y), dtype = int)
    g_matrix = np.zeros_like((size_x, size_y), dtype = int)


    for x in range(img.size[0] - 2):
        for y in range(img.size[1] - 2):
            frame = get_frame()
            x_matrix[x][y] = np.sum(np.multiply(Gx, frame))
            y_matrix[x][y] = np.sum(np.multiply(Gy, frame))
            g_matrix[x][y] = math.sqrt(pow(x_matrix[x][y], 2) + pow(y_matrix[x][y], 2))
    return (x_matrix, y_matrix, g_matrix)
            


def outline(img):
   gradients = grad_matrix(img)

   return simple_binarization(gradients[2], 60)






if __name__ == "__main__":

    srcpath = ''
    outpath = ''

    with Image.open(srcpath).convert('1') as img:
        img_a = np.array(img)
        tmp = outline(img_a)
        
        result = Image.fromarray(tmp,'L') 
        result.save(outpath)

