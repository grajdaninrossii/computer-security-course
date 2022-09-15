import code
import operator

class Al_Caesar:

    def __init__(self, stride: int = 20):
        self.__stride = stride

    __len_alpha: int = ord('z')-ord('a') # Длина алфавита
    __offset: int = ord('a')

    def crypt(self, msg: str) -> str:
        op = operator.add
        return self.create_msg(msg, op)

    def decrypt(self, code_msg: str) -> str:
        op = operator.sub
        return self.create_msg(code_msg, op)

    # Смещаем текст в зависимости от выбранного метода
    def create_msg(self, msg, op):
        return ''.join([chr((op(ord(ch),self.__stride)-self.__offset) % self.__len_alpha+self.__offset) if ch != " "  else " "  for ch in msg])

    def set_stride(self, stride: int)-> None:
        self.__stride = stride


def main():
    try:
        stride = int(input('Enter key: '))
    except ValueError:
        print('Нужно вводить целое число! Стандартное смещение(20) задано ')
        stride = 20

    msg = input('Введите сообщение: ')

    coder = Al_Caesar(stride)

    # coder.set_stride(3)

    print(msg)
    code_msg = coder.crypt(msg)
    print(code_msg)
    print(coder.decrypt(code_msg))

if __name__ == "__main__":
    main()