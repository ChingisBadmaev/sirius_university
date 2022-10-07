Задача о ракетной атаке
=======================

На карте размером $100\times100$ расположены объекты военной инфраструктуры. Каждый из объектов имеет целочисленные координаты и ценность (тоже целое число в интервале $[0,100]$). Информация обо всех военных объектах хранится в текстовом файле в следующем формате:
1. Каждая строчка содержит три целых числа, разделённых пробелом: 
```
x y w
```
Здесь `x,y` - декартовы координаты объекта, число `w` - ценность объекта.
2. В одном файле может быть записано несколько объектов, каждый объект - в новой строке.

**Задача** Необходимо написать программу для расчёта координат `(strike_x, strike_y)` нанесения оптимального ракетного удара одной ракетой (приносящего максимальный урон военной инфраструктуре), если известно, что радиус поражения ракеты составляет `R`. Программа при запуске принимает на вход два аргумента командной строки:
1. Путь к файлу, в котором лежат координаты.
2. Радиус поражения `R`.

Выдаёт на экран три числа: `x y v`
 * `x` - координата `x` нанесения удара
 * `y` - координата `y` нанесения удара
 * `v` - суммарная ценность уничтоженных объектов

**Например**: `get_target targets.txt 10`

**Требования**:
1. Программа представляет собой модуль, устанавливающийся командой `python3 setup.py install`.
2. Программа должна проверять корректность входных данных.
3. Количество целей в файле `targets.txt` может быть произвольным.

**Подсказка**: Будут ли координаты нанесения удара целыми числами?