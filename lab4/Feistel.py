import random

INT_BITS = 32
ROUNDS = 16

# -- feistel parameters
# разрядность блока данных для криптографии, менять нельзя т.к. определяет
# тип int функции фейстеля
DATA_BLOCK_WIDE = 32

#  разрядность S-блока (4)
S_BLOCK_WIDE = 4
MAGIC_ROTATE = 11

# разрядность ключа шифрования (128)
KEY_SIZE = int(ROUNDS*DATA_BLOCK_WIDE/S_BLOCK_WIDE)

# количество S-блоков в раунде (16)
S_BLOCKS = int(2*DATA_BLOCK_WIDE/S_BLOCK_WIDE)

 # -- блоки сети фейстеля
s =  [[[i for i in range(int(2**S_BLOCK_WIDE))] for _ in range(S_BLOCKS)]  for _ in range(ROUNDS)]
# s = [ROUNDS][S_BLOCKS][int(2**S_BLOCK_WIDE)] # 16,16,16


# Прописан свой генератор, ибо в лабе значения алфавита повторялись
def generate(student: int):
    random.seed(student)
    [[random.shuffle(x) for x in y] for y in s]


def str_to_int(s):
    rez = 0
    for i in range(0, 4):
        rez |= (ord(s[i])&255) << (i*8)
    return rez


def int_to_str(l):
    rez=""
    for i in range(0, 4):
        rez += chr(l&255)
        l>>=8
    return rez


# Циклический сдвиг влево
def left_rotate(n, shift):
    # Формула изменена, ибо летят разрядности
    return ((n << shift) % (1 << INT_BITS)) | (n >> (INT_BITS - shift))


def s_block(l: int, r: int, key: str) -> int:
    while len(key) != 8:
        key = '0' + key
    l_b = f'{l:032b}'
    return '0b' + "".join([f'{s[r][i*2 + int(key[i])][int("0b" + l_b[i*4:i*4+4], 2)]:04b}' for i in range(len(key))])


# По ключю работаем с блоком подстановки (замены символов S)
def get_code(l: int, r:int, pass_key: str, decrypt: bool) -> str:

    code_keys = [format(x, 'b') for x in bytearray(pass_key, 'utf-8')]
    rng_list = sorted(range(16), reverse=decrypt)

    for round in rng_list:
        l,r = r ^ left_rotate(int(s_block(l, round, code_keys[round]), 2), MAGIC_ROTATE), l
    if decrypt:
        return int_to_str(r) + int_to_str(l)
    return int_to_str(l) + int_to_str(r)

def crypt(message: str, pass_key: str) -> str:

    l, r = str_to_int(message[:4]), str_to_int(message[4:])
    return get_code(l, r, pass_key, False)


def decrypt(message: str, pass_key: str) -> str:

    r, l = str_to_int(message[:4]), str_to_int(message[4:])
    return get_code(l, r, pass_key, decrypt = True)


def main():

    generate(1)
    str = "baracuda"
    pass_key = "feistel cipher 1"
    print(f"==========\nисходные данные(2x32бит): \"{str}\"")
    print(f"ключ шифрования(128 бит): \"{pass_key}\"")
    rez = crypt(str, pass_key)
    print("зашифрованные данные: " + rez)
    rez = decrypt(rez, pass_key)
    print("расшифрованные данные: " + rez)



if __name__ == '__main__':
    main()






# def crypt(message: str, pass_key: str) -> str:

#     l, r = str_to_int(message[:4]), str_to_int(message[4:])

#     # code_keys = [format(x, 'b') for x in bytearray(pass_key, 'utf-8')]
#     # for round in range(16):
#     #     temp = r ^ left_rotate(int(s_block(l, round, code_keys[round]), 2), MAGIC_ROTATE)
#     #     r = l
#     #     l = temp
#     # return int_to_str(l) + int_to_str(r)

#     return get_code(l, r, pass_key, False)


# def decrypt(message: str, pass_key: str) -> str:

#     # code_keys = [format(x, 'b') for x in bytearray(pass_key, 'utf-8')]

#     l, r = str_to_int(message[4:]), str_to_int(message[:4])

#     # for round in reversed(range(16)):
#     #     temp = l ^ left_rotate(int(s_block(r, round, code_keys[round]), 2), MAGIC_ROTATE)
#     #     l = r
#     #     r = temp
#     # return int_to_str(l) + int_to_str(r)
#     return get_code(l, r, pass_key, True)
