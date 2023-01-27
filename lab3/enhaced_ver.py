import struct
from bitarray import bitarray # для работы с битами


from enum import Enum
from math import (
    floor,
    sin,
)

class MD5Buffer(Enum):
    A = 0x67452301
    B = 0xEFCDAB89
    C = 0x98BADCFE
    D = 0x10325476


class MD5(object):
    _string = None
    _s = [[7, 12, 17, 22], [5, 9, 14, 20], [4, 11, 16, 23], [6, 10, 15, 21]]
    _buffers = {
        MD5Buffer.A: None,
        MD5Buffer.B: None,
        MD5Buffer.C: None,
        MD5Buffer.D: None,
    }

    @classmethod
    def hash(cls, string):
        cls._string = string

        preprocessed_bit_array = cls._step_2(cls._step_1())
        cls._step_3()
        cls._step_4(preprocessed_bit_array)
        return cls._step_5()

    @classmethod
    def _step_1(cls):
        # Представим строку в виде массива бит.
        bit_array = bitarray(endian="big") # С большим концом (т.е. не инвертируем)
        bit_array.frombytes(cls._string.encode("utf-8"))

        # Добавляем в конец биты, пока их количество не будет равно 448.
        # Один бит всегда добавляем
        bit_array.append(1)
        while len(bit_array) % 512 != 448:
            bit_array.append(0)

        # По канону MD5 инвертируем массив битов
        return bitarray(bit_array, endian="little")

    @classmethod
    def _step_2(cls, step_1_result):

        # Представим получившуюся на первом виде строку в 64-битном варианте.
        length = (len(cls._string) * 8) % pow(2, 64)
        length_bit_array = bitarray(endian="little")
        length_bit_array.frombytes(struct.pack("<Q", length)) # Запаковываем нашу сформированную длину <-little-endian, Q - беззнаковый long long

        # Добавляем этот объект к исходному массиву байт.
        result = step_1_result.copy()
        result.extend(length_bit_array)
        return result

    @classmethod
    def _step_3(cls):
        # К каждому ключу буфера присваемваем значения
        for buffer_type in cls._buffers.keys():
            cls._buffers[buffer_type] = buffer_type.value

    @classmethod
    def _step_4(cls, step_2_result):
        # Определяем 4 функции для создание 32-разрядного числа
        F = lambda x, y, z: (x & y) | (~x & z)
        G = lambda x, y, z: (x & z) | (y & ~z)
        H = lambda x, y, z: x ^ y ^ z
        I = lambda x, y, z: y ^ (x | ~z)

        # Определяем функцию поворота x на n бит
        rotate_left = lambda x, n: (x << n) | (x >> (32 - n))

        # Функция для получения модуля суммы
        modular_add = lambda a, b: (a + b) % pow(2, 32)

        # Формуриуем таблицу из значений синуса. +1, так как мы начинаем с 0.
        # Используем двоичную целочисленную часть синусов целых чисел (радианы) в качестве констант:
        T = [floor(pow(2, 32) * abs(sin(i + 1))) for i in range(64)]

        # Общее количество обрабатываемых 32-разрядных слов, N, всегда кратно 16.
        N = len(step_2_result) // 32

        # Обработка блоков по 512 бит.
        for chunk_index in range(N // 16):
            # Разобьем блок на 16 слов по 32 бита
            start = chunk_index * 512
            X = [step_2_result[start + (x * 32) : start + (x * 32) + 32] for x in range(16)]

            # Переводим bitarray в int
            X = [int.from_bytes(word.tobytes(), byteorder="little") for word in X]

            # Забьем буфер короткой переменной A, B, C and D.
            A = cls._buffers[MD5Buffer.A]
            B = cls._buffers[MD5Buffer.B]
            C = cls._buffers[MD5Buffer.C]
            D = cls._buffers[MD5Buffer.D]

            # Выполним 4 круга для каждой из 16 операций
            for i in range(4 * 16):
                if 0 <= i <= 15:
                    k = i
                    temp = F(B, C, D)
                elif 16 <= i <= 31:
                    k = ((5 * i) + 1) % 16
                    temp = G(B, C, D)
                elif 32 <= i <= 47:
                    k = ((3 * i) + 5) % 16
                    temp = H(B, C, D)
                elif 48 <= i <= 63:
                    k = (7 * i) % 16
                    temp = I(B, C, D)

                # Алгоритм MD5 использует модульное сложение.
                # Обратим внимание, что здесь нам нужна временная переменная.
                # Если бы мы поместили результат в `A`, то приведенное ниже выражение `A = D` перезаписало бы его.
                # Мы также не можем переместить `A = D` ниже, потому что исходное `D` уже было бы перезаписано выражением `D = C`.
                temp = modular_add(temp, X[k])
                temp = modular_add(temp, T[i])
                temp = modular_add(temp, A)
                temp = rotate_left(temp, cls._s[i//16][i % 4])
                temp = modular_add(temp, B)

                # Смещаем значения для регистров для следующей итерации.
                A = D
                D = C
                C = B
                B = temp

            # Обновляем значения буфера согласно нашим блокам.
            cls._buffers[MD5Buffer.A] = modular_add(cls._buffers[MD5Buffer.A], A)
            cls._buffers[MD5Buffer.B] = modular_add(cls._buffers[MD5Buffer.B], B)
            cls._buffers[MD5Buffer.C] = modular_add(cls._buffers[MD5Buffer.C], C)
            cls._buffers[MD5Buffer.D] = modular_add(cls._buffers[MD5Buffer.D], D)

    @classmethod
    def _step_5(cls):
        # Переводим наши биты в обратный порядок.
        A = struct.unpack("<I", struct.pack(">I", cls._buffers[MD5Buffer.A]))[0]
        B = struct.unpack("<I", struct.pack(">I", cls._buffers[MD5Buffer.B]))[0]
        C = struct.unpack("<I", struct.pack(">I", cls._buffers[MD5Buffer.C]))[0]
        D = struct.unpack("<I", struct.pack(">I", cls._buffers[MD5Buffer.D]))[0]

        # Конкантенироуем наш буфер прежде переведя его в 16-ный формат.
        return f"{format(A, '08x')}{format(B, '08x')}{format(C, '08x')}{format(D, '08x')}"


def test():
    count_k = 0
    word = ''
    hash_table = []

    Md5 = MD5()
    for text_size in range(0, 100):
        new_char = ''
        for char_ind in range(1, 1000):
            new_char = chr(char_ind)
            if (Md5.hash(word + new_char)) in hash_table:
                # print(word + new_char, hash(word + new_char))
                count_k+=1
            hash_table.append(hash(word + new_char))
        word+=new_char
    return count_k

def main():

    Md5 = MD5()
    text: list[str] = input('Enter stride: ')
    print(Md5.hash(text))
    # print("Кол-во коллизий: ", test())

if __name__ == '__main__':
    main()