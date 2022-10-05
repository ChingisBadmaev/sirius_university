

def get_military_base_data(file):
    inFile = open(file, 'r', encoding='utf8')
    array = []
    for line in inFile:
        y = line.split()
        array.append(y)
    return array


def calculate_damage(x, y, radius, file):
    data = get_military_base_data(file)
    size_data = len(data)
    damage = 0
    for i in range(size_data):
        if (int(data[i][0]) - int(x)) ** 2 + (int(data[i][1]) - int(y)) ** 2 <= int(radius) ** 2:
            damage += int(data[i][2])
    return damage


def search_max_damage(radius, file):
    data = get_military_base_data(file)
    size_data = len(data)
    max_damage = 0
    (strike_x, strike_y) = (0, 0)
    for i in range(size_data):
        damage = calculate_damage(data[i][0], data[i][1], radius, file)
        if damage > max_damage:
            max_damage = damage
            strike_x, strike_y = data[i][0], data[i][1]
    return max_damage, int(strike_x), int(strike_y)


print('enter radius:', end=' ')
R = int(input())
print('enter filename:', end=' ')
filename = input()
print(' '.join(map(str, search_max_damage(R, filename))))
