from my_io import prompt
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from os import path
from semitone import to_semitone
from haralik import haralik, CON, LUN
from contrast import contrast

images = {
    'Bricks' : 'kirp.png',
    'Pattern' : 'oboi.png',
    'Sun' : 'sun.png'
}

if __name__ == '__main__':
    print('Выберите изображение:')
    selected_image = prompt(images)
    semitone_img = to_semitone(selected_image)
    semitone_img.save(path.join('profile','semitone', selected_image))

    semi = np.array(Image.open(path.join('profile', 'semitone', selected_image)).convert('L'))

    transformed = contrast(semi)
    transformed_img = Image.fromarray(transformed.astype(np.uint8), "L")
    transformed_img.save(path.join('profile', 'contrasted', selected_image))

    figure, axis = plt.subplots(2, 1)
    axis[0].hist(x=semi.flatten(), bins=np.arange(0, 255))
    axis[0].title.set_text('Исходное изображение')

    axis[1].hist(x=transformed.flatten(), bins=np.arange(0, 255))
    axis[1].title.set_text('Преобразованное изображение')
    plt.tight_layout()
    plt.savefig(path.join('profile', 'histograms', selected_image))

    matrix = haralik(semi.astype(np.uint8))
    result = Image.fromarray(matrix.astype(np.uint8), "L")
    result.save(path.join('profile', 'haralik', selected_image))

    t_matrix = haralik(transformed.astype(np.uint8))
    t_result = Image.fromarray(t_matrix.astype(np.uint8), "L")
    t_result.save(path.join('profile', 'haralik_contrasted', selected_image))

    print(f"CON: {CON(matrix)}")
    print(f"CON (contrasted): {CON(t_matrix)}")

    print(f"LUN: {LUN(matrix)}")
    print(f"LUN (contrasted): {LUN(t_matrix)}")
