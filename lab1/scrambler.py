import random as rand
import string

charset = ' qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNMйцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'+\
'1234567890!@#$%^&*().?,'

def char_2_num(s: str) -> int:
    index = charset.index(s)
    return index

def num_2_char(i: int) -> str:
    char = charset[i]
    return char

def random_array(l: int = 10, seed: int = 2) -> list[int]:
    a = 45
    c = 21
    m = len(charset)
    rnd = lambda seed: (a * seed + c) % m

    rez = []
    for i in range(l):
        seed = rnd(seed)
        rez.append(seed)
    return rez

def scrambler(msg: str, base: int = 31)->str:
    key = random_array(len(msg), base)
    codes = map(char_2_num, msg)

    return ''.join([num_2_char(code ^key[index]) if code ^key[index] < len(charset) else num_2_char(code) for index, code in enumerate(codes)])

print(len(charset))

message = 'kek'
smessage = scrambler(message)

print(message)
print(smessage)
print(scrambler(smessage))