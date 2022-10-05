import numpy as np


def key_for_fort(data):
    return data[0] ** 2 + data[1] ** 2


f = open('dataset_1.txt', 'w')
array = list(np.random.uniform(0, 100, (10000, 3)))
array.sort(key=key_for_fort)
for item in array:
    f.write(' '.join(map(str, list(map(int, item)))) + '\n')
