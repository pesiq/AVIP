import pandas as pd
from generate import symbols


if __name__ == '__main__':
    features = pd.read_csv('./results/features.csv')
    for index, row in features.iterrows():
        str = \
        """
## Символ {letter}

![Letter](./lab05/letters/{letter}.bmp), ![Letter](./lab05/results/profiles/x/{letter}.png) ![Letter](./lab05/results/profiles/y/{letter}.png)\\

Признаки:
- Вес чёрного = {weight}
- Нормированный вес чёрного = {nweight}
- Центр масс = ({centerx}, {centery})
- Нормированный центр масс = ({ncenterx}, {ncentery})
- Моменты инерции = ({inertiax}, {inertiay})
- Нормированные моменты инерции = ({ninertiax}, {ninertiay})
        """.format(
            letter=row.letter,
            weight=row.weight,
            nweight=row.relative_weight,
            centerx=row.center_x,
            centery=row.center_y,
            ncenterx=row.relative_center_x,
            ncentery=row.relative_center_y,
            inertiax=row.inertia_x,
            inertiay=row.inertia_y,
            ninertiax=row.relative_inertia_x,
            ninertiay=row.relative_inertia_y,
        )
        print(str)
