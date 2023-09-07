import pandas as pd
import numpy as np
from PIL import Image
from features import FeatureImage
import csv
from math import sqrt


def dist(vector1, vector2):
    assert len(vector1) == len(vector2)
    sum_square_diff = 0

    for coord1, coord2 in zip(vector1, vector2):
        sum_square_diff += (coord1 - coord2) ** 2
    return sum_square_diff


def levenstein_distance(profile1, profile2):
    M = profile1.shape[0]
    N = profile2.shape[0]
    D = np.zeros((M + 1, N + 1))
    for j in range(1, N + 1):
        D[0, j] = D[0, j - 1] + 1
    for i in range(1, M + 1):
        D[i, 0] = D[i - 1, 0] + 1
        for j in range(1, N + 1):
            D[i, j] = min(
                D[i - 1, j] + 1,
                D[i, j - 1] + 1,
                D[i - 1, j - 1] + abs(profile1[i - 1] - profile2[j - 1])
            )
    # print(D)
    return D[M, N]


def proximity(vector1, vector2):
    return 1 / (1 + dist(vector1, vector2))


feature_names = ['relative_' + name for name in
                 ['weight_I', 'weight_II', 'weight_III', 'weight_IV', 'center_x', 'center_y', 'inertia_x', 'inertia_y']]
target = 'ENGEVEZEKUŞÜMITTIRKALBIMIZDEHIÇSUSMAZ'
symbols = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTÜVYZ"


if __name__ == '__main__':
    features = pd.read_csv('./profile/features.csv')
    sentence = ""
    results = []

    for i in range(len(target)):
        symbol = FeatureImage(Image.open(f'./result/segmented/{i}.png'), invert=True)
        feature_vector = [
            symbol.relative_weight_I(),
            symbol.relative_weight_II(),
            symbol.relative_weight_III(),
            symbol.relative_weight_IV(),
            symbol.relative_center(1),
            symbol.relative_center(0),
            symbol.relative_inertia(1),
            symbol.relative_inertia(0)
        ]

        distances = features.apply(
            lambda feature_symbol: dist(feature_symbol[feature_names], feature_vector), axis=1
        )

        proximities = distances.apply(
            lambda distance: 1 - distance / distances.max()
        )

        feature_images = {letter: FeatureImage(Image.open(f"./letters/{letter}.bmp")) for i, letter in enumerate(symbols)}
        proximities = pd.concat([features.letter, proximities], axis=1)
        proximities.columns = ['letter', 'proximity']
        proximities = proximities.sort_values('proximity', ascending=False)
        proximities = proximities.reset_index(drop=True)

        delta = 0.9
        potential_letters = proximities[proximities.proximity > delta]
        if len(potential_letters) == 0:
            continue
        proximities['x_profile_distance'] = potential_letters.apply(
            lambda potential_symbol:
            levenstein_distance(symbol.profile_norm(0), feature_images[potential_symbol.letter].profile_norm(0)),
            axis=1
        )

        proximities['y_profile_distance'] = potential_letters.apply(
            lambda potential_symbol:
            levenstein_distance(symbol.profile_norm(1), feature_images[potential_symbol.letter].profile_norm(1)),
            axis=1
        )

        potential_letters = proximities[proximities.proximity > delta]
        proximities['profile_distance'] = potential_letters.apply(
            lambda potential_symbol:
            np.sqrt(potential_symbol.x_profile_distance ** 2 + potential_symbol.y_profile_distance ** 2),
            axis=1
        )

        potential_letters = proximities[proximities.proximity > delta]
        proximities['profile_proximity'] = potential_letters.apply(
            lambda potential_symbol:
            1 - potential_symbol.profile_distance / potential_letters.profile_distance.max(),
            axis=1
        )

        potential_letters = proximities[proximities.proximity > delta]
        proximities = proximities.sort_values(['profile_proximity', 'proximity'], ascending=False)
        proximities = proximities.reset_index(drop=True)
        results.append(proximities.apply(
            lambda guessed_letter:
            (guessed_letter['letter'], guessed_letter['proximity'])
            , axis=1
        ))

        sentence += proximities['letter'][0]
        print(sentence)

    res = pd.DataFrame(results)
    res.to_csv('result/result.csv')

    correct_guesses = 0
    for i, (expected, actual) in enumerate(zip(target, sentence)):
        correct_guesses += (expected == actual)
        if expected != actual:
            print("Mistake: index =", str(i) + ", expected:", expected, "but got", actual)

    print(correct_guesses)
    print('Accuracy:', correct_guesses / 37)