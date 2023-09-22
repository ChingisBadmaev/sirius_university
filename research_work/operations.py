
import pandas as pd
import numpy as np


def neutralize(alpha):
    return alpha.add(-alpha.mean(axis=1), axis=0)


def normalize(alpha):
    return alpha.div(abs(alpha).sum(axis=1), axis=0)


def truncate(alpha, max_weight, coef):
    alphas = alpha.copy()
    signs = (alphas / np.abs(alphas))
    alphas[np.abs(alphas) > max_weight * coef] = max_weight * coef * signs
    return normalize(neutralize(alphas))


def ranking(alpha):
    return normalize(neutralize(alpha.rank(axis=1) / (len(alpha) - 1)))


def cut_outliers(alpha, coef):
    alphas = alpha.copy()
    alphas[alphas > np.quantile(alphas, coef)] = 0
    alphas[alphas < np.quantile(alphas, 1 - coef)] = 0
    return normalize(neutralize(alphas))


def cut_middle(alpha, eps):
    alphas = alpha.copy()
    alphas[(alphas < np.quantile(alphas, 0.5 + eps)) & (alphas > np.quantile(alphas, 0.5 - eps))] = 0
    return normalize(neutralize(alphas))


def get_decay_vect(alpha, d, k):
    if d < k:
        return 'Error'
    temp = np.zeros(alpha.shape[1])
    for i in range(k):
        temp += ((k - i) / k) * alpha.iloc[d - i]
    return temp


def get_decay_alpha(alpha, d, k):
    alpha_new = alpha.copy().iloc[0 : d]
    for i in range(d, len(alpha)):
        alpha_new.loc[len(alpha_new.index)] = get_decay_vect(alpha, i, k)
    alpha_new.index = alpha.iloc[0 : len(alpha_new.index)].index
    return normalize(neutralize(alpha_new))


def get_alpha_mul_ts_tank_data(alpha, ts_tank_data):
    return normalize(neutralize(alpha.copy() * ts_tank_data))
