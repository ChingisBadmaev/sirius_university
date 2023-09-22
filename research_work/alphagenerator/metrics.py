import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import scipy
from tqdm import tqdm


def get_turnover(alpha, isyear=0):
    turnover_days = abs(alpha.diff(periods=1)).sum(axis=1)
    if isyear == 1:
        return turnover_days
    return turnover_days.groupby(alpha.index.year).mean()


def get_sharpe_coef(days_pnl):
    ans = pd.DataFrame()
    ans['coef_sharpe'] = days_pnl.groupby(days_pnl.index.year).apply(lambda x : np.sqrt(len(x) - 1) * np.mean(x) / np.std(x))
    return ans


def get_pnl(returns, alpha, isyear=0):
    returns = returns.iloc[2:]
    pnl = alpha.reset_index(drop=True).mul(returns.reset_index(drop=True), axis=0).sum(axis=1)
    ans = pd.DataFrame()
    ans['pnl'] = pnl
    ans = ans.set_index(alpha.index).shift(1)
    if isyear == 1:
        return ans
    return ans.set_index(alpha.index).groupby(alpha.index.year).sum()


def get_drawdown(pnl):
    pnl_index =  pnl.index
    pnl = np.array(pnl)
    drawdown = 0
    loc_max = pnl[0]
    day_high = 0
    day_low = 0
    for i in range(1, len(pnl)):
        if pnl[i] > loc_max:
            loc_max = pnl[i]
            day_high = i
        if loc_max - pnl[i] > drawdown:
            drawdown = float(loc_max - pnl[i])
            day_low = i
    return drawdown, pnl_index[day_high].strftime("%d.%m.%Y"), pnl_index[day_low].strftime("%d.%m.%Y")


def get_drawdown_years(pnl_cum):
    return pnl_cum.groupby(pnl_cum.index.year).apply(lambda x: get_drawdown(x))



def alpha_stats(data_returns, alpha):
    days_pnl = get_pnl(data_returns, alpha, 1).fillna(0)['pnl']
    returns_table = pd.DataFrame()
    returns_table['years_pnl_cum'] = get_pnl(data_returns, alpha)
    returns_table['turnover'] = get_turnover(alpha)
    returns_table['sharpe_coef'] = get_sharpe_coef(days_pnl)
    returns_table['drawdown'] = get_drawdown_years(days_pnl.cumsum()).apply(lambda x: x[0])
    returns_table['drawdown_day_start'] = get_drawdown_years(days_pnl.cumsum()).apply(lambda x: x[1])
    returns_table['drawdown_day_end'] = get_drawdown_years(days_pnl.cumsum()).apply(lambda x: x[2])
    print(days_pnl.sum())
    days_pnl.cumsum().plot()
    plt.grid(True)
    plt.show()
    return returns_table