import pandas as pd


def process_row(source):
    x_data = []
    y_data = []
    z_data = []
    for item in source.split(','):
        elem = item.strip(' = ')
        if elem[0] == 'x':
            x_data.append(elem[3:])
        if elem[0] == 'y':
            y_data.append(elem[3:])
        if elem[0] == 'z':
            z_data.append(elem[3:])
    return x_data, y_data, z_data


print('input your data:')
input_data = input()
df = pd.DataFrame(process_row(input_data)).T
df.rename({0: 'x', 1: 'y', 2: 'z'}, axis=1, inplace=True)
df['x'] = df['x'].astype(float)
df['z'] = df['z'].astype(int)
df.to_csv('data_from_console', index=False)
