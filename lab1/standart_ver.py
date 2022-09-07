import code


class Al_Caesar:

    def __init__(self, stride: int = 20):
        self.__stride = stride

    def crypt(self, msg: str) -> str:
        code_msg = ''.join([chr(ord(ch)+self.__stride) if ch != " "  else " "  for ch in msg])
        return code_msg

    def decrypt(self, code_msg: str) -> str:
        msg = ''.join([chr(ord(ch)-self.__stride) if ch != " "  else " " for ch in code_msg])
        return msg

    def set_stride(self, stride: int)-> None:
        self.__stride = stride


def main():
    try:
        stride = int(input('Enter stride: '))
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