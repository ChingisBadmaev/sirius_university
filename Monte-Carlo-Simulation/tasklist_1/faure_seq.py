import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
from tqdm import tqdm
import math
from scipy.linalg import pascal

def convert_number_system(number, base):
    ans = []
    temp = number
    while number >= base:
        ans.append(number % base)
        number = number // base
    ans.append(number)
    return temp, ans, sum([ans[i] / base ** (i + 1) for i in range(len(ans))])


def get_faure_c_matrix(i, k, base):
    r = len(convert_number_system(k, base)[1])
    C = np.zeros((r, r))
    pascal_matrix = pascal(r, kind='upper')
    for j in range(r):
        C_vector = []
        for l in range(r):
            if l >= j:
                C_vector.append(pascal_matrix[j][l] * (i ** (l - j)))
            else:
                C_vector.append(0)
        C[j] = C_vector
    return C


# надо правильно считать y
def get_faure_y(i, k, base):
    a = convert_number_system(k, base)[1]
    r = len(a)
    return  np.apply_along_axis(lambda x: x % base, 0, get_faure_c_matrix(i - 1, k, base).dot(a))

def get_faure_seq(d, max_number, base):
    faure_sequence = np.zeros((max_number, d))
    for k in tqdm(range(1, max_number + 1)):
        a = convert_number_system(k, base)[1]
        r = len(a)
        x = np.zeros(d)
        for i in range(1, d + 1):
            y = get_faure_y(i, k, base)
            x[i - 1] = sum([y[j] * pow(base, -j - 1) for j in range(r)])
            faure_sequence[k - 1][i - 1] = x[i - 1]
    return faure_sequence.T


def discrepancy(sequence):
    min_index_0 = np.argmin(sequence[0])
    min_index_1 = np.argmin(sequence[1])

    vol_0 = sequence[0][min_index_0] * sequence[1][min_index_0]
    vol_1 = sequence[0][min_index_1] * sequence[1][min_index_1]

    vol_A = max(vol_0, vol_1)
    sup = abs(vol_A - 1 / len(sequence[0]))
    return sup