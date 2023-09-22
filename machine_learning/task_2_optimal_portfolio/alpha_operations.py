
import pandas as pd
import numpy as np


def neutralize(alpha):
    return alpha.add(-alpha.mean(axis=1), axis=0)


def normalize(alpha):
    return alpha.div(abs(alpha).sum(axis=1), axis=0)


def get_alpha_from_vector(alpha):
    alpha = alpha - alpha.mean()
    alpha = alpha / sum(abs(alpha))
    return alpha

def truncate(alpha, max_weight, coef):
    alphas = alpha.copy()
    signs = (alphas / np.abs(alphas))
    alphas[np.abs(alphas) > max_weight * coef] = max_weight * coef * signs
    return normalize(neutralize(alphas))


def ranking(alpha):
    return normalize(neutralize(alpha.rank(axis=1) / (alpha.shape[1] - 1)))


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
    ts_rank_alpha = alpha.copy() * ts_tank_data
    ts_rank_alpha.iloc[:19] = alpha.copy().iloc[:19]
    return normalize(neutralize(ts_rank_alpha))

# ts_rank
def ts_rank_alpha(data, size_window):
    ans = []
    for i in range(data.shape[0] - size_window + 1):
        ans.append(data.iloc[i:i + size_window].rank(axis=0).iloc[-1] / size_window)
    return normalize(neutralize(pd.concat([data.iloc[:size_window - 1], pd.DataFrame(ans)])))

def ts_rank(data, size_window):
    ans = []
    for i in range(data.shape[0] - size_window + 1):
        ans.append(data.iloc[i:i + size_window].rank(axis=0).iloc[-1] / size_window)
    return pd.concat([data.iloc[:size_window - 1], pd.DataFrame(ans)])

# ts_stddev
def ts_stddev(data, size_window):
    ans = []
    date = data.index[size_window - 1:]
    for i in range(data.shape[0] - size_window + 1):
        ans.append(data.iloc[i:i + size_window].std(axis=0))
    return pd.DataFrame(ans, index=date)

def ts_stddev_alpha(data, size_window):
    ans = []
    date = data.index[size_window - 1:]
    for i in range(data.shape[0] - size_window + 1):
        ans.append(data.iloc[i:i + size_window].std(axis=0))
    return normalize(neutralize(pd.DataFrame(ans, index=date)))

# days_vwap
def vwap(data, data_volume, size_window):
    size_window = 10
    ans = []
    date = data.index[size_window - 1:]
    for i in range(data.shape[0] - size_window + 1):
        ans.append((data.iloc[i:i + size_window] * data_volume.iloc[i:i + size_window]).sum() / (data_volume.iloc[i:i + size_window]).sum())
    return pd.DataFrame(ans, index=date)