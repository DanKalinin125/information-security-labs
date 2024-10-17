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

def find_symbol_by_point_in_alphabet(alphabet, point):
    for row in alphabet:
        if int(row[2]) == point[0] and int(row[3]) == point[1]:
            return row[1]
    print(f'Ошибка: точка {point} не найдена в исходном алфовите')
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
    close_message_text = """
                    {(618, 206), (426, 662)}; {(72, 254), (67, 667)};
                    {(286, 136), (739, 574)}; {(16, 416), (143, 602)};
                    {(618, 206), (313, 203)}; {(618, 206), (114, 607)};
                    {(618, 206), (438, 711)}; {(188, 93), (573, 168)}
                    """
    nb = 34

    # Обработка шифртекста
    close_message = []
    for part in close_message_text.split(";"):
        part = part.strip().replace("{", "").replace("}","").replace("(","").replace(")","")
        part_split = part.split(", ")
        close_message.append(([int(part_split[0]), int(part_split[1])], [int(part_split[2]), int(part_split[3])]))

    print("-- Исходные данные --")
    print(f'Шифртекст = {close_message}')
    print(f'Закрытый ключ B = {nb}')
    print()

    #Дешифрование сообщения
    print("-- Дешифрование --")
    open_message = ""
    Pm_array = []
    for kG, Cm in close_message:
        print(f'Дешифруем часть шифртекста {Cm}, kG = {kG}')

        nbkG = calc_k_multiply_point(p, E, nb, kG, "*kG")
        print(f'{nb}*kG = {nbkG}')

        nbkG[1] = p - nbkG[1]
        print(f'-{nb}*kG = {nbkG}')

        Pm = sum_points_elliptic_curve(p, E, Cm, nbkG)
        print(f'Pm = Cm - nb(kG) = {Cm} + {nbkG} = {Pm}')

        symbol = find_symbol_by_point_in_alphabet(alphabet, Pm)
        print(f'Символ {Pm} = \'{symbol}\'')

        open_message += symbol
        Pm_array.append(Pm)
        print()

    print("-- Результат --")
    for i in range(len(close_message)):
        kG = close_message[i][0]
        Cm = close_message[i][1]
        Pm = Pm_array[i]
        symbol = open_message[i]

        print(f'kG = {kG}, Cm = {Cm} ----> Pm = {Pm} -----> \'{symbol}\'')
    print(f"Дешифрованное сообщение = \'{open_message}\'")
