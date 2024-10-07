import math

def fermats_method(N, e):
    """Вычисляет закрытый ключ и параметры шифрования методом Ферма"""

    print("-- Метод Ферма --")
    n = math.trunc(math.sqrt(N)) + 1
    print(f'n = [sqrt(N)] + 1')

    i = 1
    while True:
        t = n + i
        w = pow(t, 2) - N

        print(f't_{i} = n + i = {n} + {i} = {t}')
        print(f'w_{i} = t_{i}^2 - N = {pow(t, 2)} - {N} = {w}')

        if (math.sqrt(w) % 1 != 0):
            # w - не квадрат целого числа
            print(f'w_{i} - не квадрат целого числа')
            i += 1
        else:
            # w - квардрат целого числа
            print(f'w_{i} - квадрат целого числа')
            break

    p = t + int(math.sqrt(w))
    q = t - int(math.sqrt(w))
    euler_function = (p - 1) * (q - 1)
    d = pow(e, -1, euler_function)

    print()
    print(f'p = t + sqrt(w) = {t} + {int(math.sqrt(w))} = {p}')
    print(f'q = t - sqrt(w) = {t} - {int(math.sqrt(w))} = {q}')
    print(f'euler_function = (p - 1)(q - 1) = {euler_function}')
    print(f'd = e^(-1) mod euler_function = {d}')

    return p, q, euler_function, d


def decode_part(N, d, part):
    """Декодирует часть сообщения в текст"""

    int_decoded_part = pow(part, d, N)
    return int_decoded_part.to_bytes(4, byteorder='big').decode('cp1251')


def decode(N, d, C):
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
        decoded_part = decode_part(N, d, part)
        original_message += decoded_part
        print(f'Декодирована часть {part} -----> {decoded_part}')

    return original_message


if __name__ == '__main__':
    # Описание варианта
    N = 89318473363897
    e = 2227661
    C = """
        3403106899606
        26746900101177
        67769260919924
        77873792354218
        15782947730235
        15100267747684
        28877721728826
        62898555111378
        4989704651236
        55293402838380
        4108112294245
        8492269964172
        """

    print("-- Исходные данные --")
    print(f'N = {N}')
    print(f'e = {e}')
    print(f'C = \"{C}\"')
    print("\n")

    # Вычисляем закрытый ключ и требуемые параметры
    p, q, euler_function, d = fermats_method(N, e)

    print("\n")

    # Декодируем сообщение
    original_message = decode(N, d, C)
    print(f'\nОригинальное сообщение - \"{original_message}\"')