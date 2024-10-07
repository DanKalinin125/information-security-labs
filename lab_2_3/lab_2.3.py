def extended_euclidean_algorithm(e1, e2):
    if e2 == 0:
        print(f'Расш. алг. Евклида (e1 = {e1}, e2 = {e2}) --> r = {1}, s = {0}')
        return 1, 0
    else:
        print(f'Расш. алг. Евклида (e1 = {e1}, e2 = {e2})')
        r, s = extended_euclidean_algorithm(e2, e1 % e2)
        print(f'Расш. алг. Евклида (e1 = {e1}, e2 = {e2}) --> r = {s}, s = {r - s * (e1 // e2)}')
        return s, r - s * (e1 // e2)

def decode(N, C1, C2, r, s):
    """Декодирует полученные сообщение в текст"""

    print("-- Дешифрование сообщения --")

    # Раздаляем закодированное сообщение на части и подготавливаем их
    raw_parts_C1 = C1.split("\n")
    parts_C1 = []
    for i in range(len(raw_parts_C1)):
        if raw_parts_C1[i].strip() != "":
            parts_C1.append(int(raw_parts_C1[i].strip()))

    raw_parts_C2 = C2.split("\n")
    parts_C2 = []
    for i in range(len(raw_parts_C2)):
        if raw_parts_C2[i].strip() != "":
            parts_C2.append(int(raw_parts_C2[i].strip()))

    if (len(parts_C1) != len(parts_C2)):
        print("Дешифрование прервано - Ввод C1 и C2 с разным количеством частей")
        exit(1)

    # Декодируем каждую часть
    original_message = ""
    for i in range(len(parts_C1)):
        y1 = parts_C1[i]
        y2 = parts_C2[i]

        int_decoded_part = pow(y1, r, N)*pow(y2, s, N) % N
        decoded_part = int_decoded_part.to_bytes(4, byteorder='big').decode('cp1251')
        original_message += decoded_part
        print(f'Декодирована часть C1 = {y1} и C2 = {y2} -----> {int_decoded_part} -----> {decoded_part}')

    return original_message

if __name__ == '__main__':
    # Описание варианта
    N = 535598392051
    e1 = 455341
    e2 = 396971
    C1 = """
        444982997352
        277831853272
        133187882628
        331361392426
        273206302188
        470299046774
        168157171491
        258737286129
        312335302650
        489235057221
        427689116872
        418723605534
        135022585485
        """
    C2 = """
        358696089912
        360292494113
        91390259562
        534590606880
        193203217609
        166702058071
        68207231399
        487524624411
        325841328769
        533726724224
        369967614519
        247201359991
        478832067683
        """

    print("-- Исходные данные --")
    print(f'N = {N}')
    print(f'e1 = {e1}')
    print(f'e2 = {e2}')
    print(f'C1 = \"{C1}\"')
    print(f'C2 = \"{C2}\"')
    print()

    # Решаем уравнение  r*e1 + s*e2 = 1
    print("-- Расширенный алгоритм Евклида --")
    r, s = extended_euclidean_algorithm(e1, e2)
    print(f'r = {r}')
    print(f's = {s}')
    print(f'r*e1 + s*e2 = {r}*{e1} + {s}*{e2} = {r*e1 + s*e2}')
    print()

    # Декодируем сообщение
    original_message = decode(N, C1, C2, r, s)
    print(f'\nОригинальное сообщение - \"{original_message}\"')