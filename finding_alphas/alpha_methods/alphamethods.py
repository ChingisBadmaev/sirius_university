import numpy as np

def get_returns(data):
    temp = np.lib.stride_tricks.sliding_window_view(data, (1,2))
    lambda_returns = lambda x: x[..., 1] / x[..., 0]
    returns = lambda_returns(temp).reshape(2436, 1256)
    return returns


def correct_wrong_values(data):
    err_coord_low = np.where(get_returns(data) <= (1 / 8))
    err_coord_high = np.where(get_returns(data) >= 8)
    for i in range(len(err_coord_low[0])):
        id_low_0 = err_coord_low[0][i]
        id_low_1 = err_coord_low[1][i]
        
        id_high_0 = err_coord_high[0][i]
        id_high_1 = err_coord_high[1][i]

        if 0.5 < data[id_high_0][id_low_1] / data[id_high_0][id_high_1 + 1] < 2:        # if the price has dropped
            data[id_high_0][id_high_1] = data[id_high_0][id_high_1 + 1]

        if 0.5 < data[id_high_0][id_high_1] / data[id_high_0][id_low_1 + 1] < 2:        # If the price went up
            data[id_high_0][id_low_1] = data[id_high_0][id_low_1 + 1]
