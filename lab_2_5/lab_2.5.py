import csv
def read_alphabet():
    alphabet = []
    with open("../resources/alphabet.csv", encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        count = 0
        for row in file_reader:
            if count != 0:
                alphabet.append([int(row[0]), row[1], int(row[2]), int(row[3])])
            count += 1
    return alphabet

def find_symbol_point_in_alphabet(alphabet, symbol):
    for row in alphabet:
        if row[1] == symbol:
            return row[2], row[3]
    print(f'Ошибка: символ {symbol} не найден в исходном алфовите')
    exit(1)

def sum_points_elliptic_curve(p, E, P, Q):
    # Вычисляем лямбда
    l = 0
    if P[0] == Q[0] and P[1] == Q[1]:
        l_top = (3*P[0]**2 + E[0]) % p
        l_bottom = (2*P[1]) % p
        for res in range(p+1):
            if (res == p):
                print("Ошибка: невозможно найти модуль от деления в процессе вычисления lambda")
                exit(1)
            if ((l_bottom * res) % p) == (l_top % p):
                l = res
                break
    else:
        l_top = (Q[1] - P[1]) % p
        l_bottom = (Q[0] - P[0]) % p
        for res in range(p + 1):
            if (res == p):
                print("Ошибка: невозможно найти модуль от деления в процессе вычисления lambda")
                exit(1)
            if ((l_bottom * res) % p) == (l_top % p):
                l = res
                break

    if (l % 1 == 0):
        l = int(l)
    else:
        print(f'Ошибка: lambda = {l}, не целое цисло!')
        exit(1)
    #print(f'lambda = {l}')

    # Вычисляем координаты
    x = (pow(l, 2, p) - P[0] - Q[0]) % p
    y = (l*(P[0] - x) - P[1]) % p
    return [x, y]

def calc_k_multiply_point(p, E, k, Point, point_name):
    iPoint = Point
    for i in range(2, k+1):
        iPoint = sum_points_elliptic_curve(p, E, iPoint, Point)
        #print(f'{i}{point_name} = {iPoint}')
    return iPoint


if __name__ == '__main__':
    # Константы
    p = 751
    E = [-1, 1]
    G = [0, 1]
    alphabet = read_alphabet()

    # Описание варианта
    open_message = "симметрия"
    Pb = [179, 275]
    k_array_A = [11, 17, 18, 19, 16, 6, 12, 8, 2]

    print("-- Исходные данные --")
    print(f'Открытый текст = {open_message}')
    print(f'Открытый ключ B = {Pb}')
    print(f'Значения случайных чисел k для букв открытого текста = {k_array_A}')
    print()

    # Проверяем корректность введенных данных
    if len(open_message) != len(k_array_A):
        print("Ошибка: длина массива k и открытого текста должна быть равной")
        exit(1)

    # Шифруем сообщение
    print("-- Шифрование --")
    close_message = []
    for i in range(len(open_message)):
        symbol = open_message[i]
        k = k_array_A[i]
        print(f'Шифруем символ \'{symbol}\', k = {k}')

        # Код символа из алфавита
        Pm = find_symbol_point_in_alphabet(alphabet, symbol)
        print(f'Pm = {Pm}')

        # Открытый ключ A
        kG = calc_k_multiply_point(p, E, k, G, "G")
        print(f'{k}G = {kG}')

        # Шифрование символа
        kPb = calc_k_multiply_point(p, E, k, Pb, "Pb")
        print(f'{k}Pb = {kPb}')

        Cm = sum_points_elliptic_curve(p, E, Pm, kPb)
        print(f'Cm = Pm + kPb = {Pm} + {kPb} = {Cm}')
        print()
        close_message.append((kG, Cm))

    print("-- Результат --")
    for i in range(len(open_message)):
        symbol = open_message[i]
        k = k_array_A[i]
        tmp = "{" + str(close_message[i][0]) + ", " + str(close_message[i][1]) + "}"
        print(f'Символ {symbol}, k = {k} ----> Cm = {tmp}')