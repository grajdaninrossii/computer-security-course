# dict выше python 3.7, иначе порядок поломается

from random import shuffle
from data import *

# Инициализируем алфавит
a: int = ord('а')
alphabet: str = ''.join([chr(i) for i in range(a,a+6)] + [chr(a+33)] + [chr(i) for i in range(a+6,a+32)])

# Получаем частоту букв
def get_freq_char(number_text: int) -> list[str]:
    text: str = data_text['т'+str(number_text)]
    freq_dict:dict[str:int] = dict(sorted({k: text.count(k) for k in alphabet}.items(), key=lambda item: item[1], reverse=True))
    # sum_all_step_unique_char:int = sum(freq_dict.values())
    freq_dict:dict[str:float] = freq_dict.keys()
    return freq_dict

# Получаем словарь типа буква_шифр: буква
def merge_char_list(lst_alpha: list, lst_text: list) -> dict:
    return dict(map(lambda x, y: (x,y), lst_text, lst_alpha))

# Раскодируем
def get_text(number_text: int, dict_char: dict) -> str:
    text: str = data_text['т'+str(number_text)]
    return ''.join([dict_char[ch] if ch in alphabet else ch for ch in text])

def get_decrypt_text(text_number: int) -> str:
    freq_dict:dict[str:float] = get_freq_char(text_number)
    merged_dict = merge_char_list(data_char[text_number - 1].keys(), freq_dict)
    print(merged_dict)

    return get_text(text_number, merged_dict)

def main():
    text_number: int = 1
    try:
        text_number: int = int(input('Введите номер текста (1-5): '))
    except ValueError:
        pass
    print(get_decrypt_text(text_number))

if __name__=="__main__":
    main()