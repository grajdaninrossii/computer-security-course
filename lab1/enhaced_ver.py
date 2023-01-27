import string
import random

class Al_Changed:

    __alphabet: str = string.ascii_lowercase # Сохраняем алфавит

    def __init__(self, seed: int = 3):
        self.__seed = seed

    def crypt(self, msg: str) -> str:

        # Инициализируем генерацию случайных чисел и получаем алфавит подмены
        random.seed((len(msg)*2 + self.__seed) // (self.__seed+1))
        shuffle_alphabet = list(self.__alphabet)
        random.shuffle(shuffle_alphabet)

        # Переводим
        code_msg = ''.join([shuffle_alphabet[self.__alphabet.index(ch)] if ch != " "  else " "  for ch in msg])
        return code_msg

    def decrypt(self, code_msg: str) -> str:

        # Инициализируем генерацию случайных чисел и получаем алфавит подмены
        random.seed((len(code_msg)*2 + self.__seed) // (self.__seed+1))
        shuffle_alphabet = list(self.__alphabet)
        random.shuffle(shuffle_alphabet)

        # Переводим
        msg = ''.join([self.__alphabet[shuffle_alphabet.index(ch)] if ch != " "  else " " for ch in code_msg])
        return msg


def main():

    try:
        seed = int(input('Enter stride: '))
    except ValueError:
        print('Нужно вводить целое число! Стандартное смещение(20) задано ')
        seed = 20

    msg = input('Введите сообщение: ')

    coder = Al_Changed(seed)

    code_msg = coder.crypt(msg)
    print(code_msg)
    print(coder.decrypt(code_msg))

if __name__ == '__main__':
    main()