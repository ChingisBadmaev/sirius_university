import pandas as pd


def file_lines_iterator(filename):
    with open(filename, 'r') as f:
        for row in f:
            yield row


def process_row(source):
    x_data = []
    y_data = []
    z_data = []
    for row in source:
        for item in row.split(','):
            elem = item.strip(' = ')
            if elem[0] == 'x':
                x_data.append(elem[3:])
            if elem[0] == 'y':
                y_data.append(elem[3:])
            if elem[0] == 'z':
                z_data.append(elem[3:][0:-1])  # [0:-1] чтобы не было '\n'
    return x_data, y_data, z_data


print('enter the filename:')
filename = input()
df = pd.DataFrame(process_row(file_lines_iterator(filename))).T

df.rename({0: 'x', 1: 'y', 2: 'z'}, axis=1, inplace=True)
df['x'] = pd.to_numeric(df['x'])
df['z'] = pd.to_numeric(df['z'])
df.to_csv(f'dataset_after_change.csv', index=False)
