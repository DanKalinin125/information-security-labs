def re_encryption_method(N, e, C):
    """Определение порядка числа e"""
    print("-- Метод повторного шифрования --")

    # Выбираем первую часть, на которой будем искать степерь повтороного кодирования
    raw_parts = C.split("\n")
    y = 0
    for i in range(len(raw_parts)):
        if raw_parts[i].strip() != "":
            y = int(raw_parts[i].strip())
            break

    # Выполняем повторное шифрование
    y_i = y
    i = 1
    while True:
        y_i = pow(y_i, e, N)
        i+=1

        if (y_i == y):
            break

    print(f'y_{i} = y = {y_i}')
    return i - 2 #Порядок числа e


def decode(N, e, C, m):
    """Декодирует полученное сообщение в текст"""

    print("-- Дешифрование сообщения --")

    # Раздаляем закодированное сообщение на части и подготавливаем их
    raw_parts = C.split("\n")

    parts = []
    for i in range(len(raw_parts)):
        if raw_parts[i].strip() != "":
            parts.append(int(raw_parts[i].strip()))

    # Декодируем каждую часть
    original_message = ""
    for part in parts:
        int_decoded_part = pow(part, pow(e, m), N)
        decoded_part = int_decoded_part.to_bytes(4, byteorder='big').decode('cp1251')
        original_message += decoded_part
        print(f'Декодирована часть {part} -----> y_{m+1} = {int_decoded_part} -----> {decoded_part}')

    return original_message

if __name__ == '__main__':
    # Описание варианта
    N = 489740760623
    e = 892627
    C = """
        237434928568
        89382477865
        257542914775
        153947910848
        219678068406
        166466311168
        49516725114
        55375254449
        370796045103
        322927050068
        196366079994
        39243100230
        299525662956
        """

    print("-- Исходные данные --")
    print(f'N = {N}')
    print(f'e = {e}')
    print(f'C = \"{C}\"')
    print()

    # Определяем порядок числа e
    m = re_encryption_method(N, e, C)
    print(f'x = y_{m + 1}')
    print(f'Порядок числа e = {m}')
    print()

    # Декодируем сообщение
    original_message = decode(N, e, C, m)
    print(f'\nОригинальное сообщение - \"{original_message}\"')