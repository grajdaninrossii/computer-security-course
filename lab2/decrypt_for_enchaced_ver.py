# dict выше python 3.7, иначе порядок поломается

from random import shuffle
from data import *
from collections import Counter

# Инициализируем алфавит
a: int = ord('а')
alphabet: str = ''.join([chr(i) for i in range(a,a+6)] + [chr(a+33)] + [chr(i) for i in range(a+6,a+32)])

# Получаем частоту букв
def get_freq_char(number_text: int) -> dict[str:float]:
    text: str = data_text['т'+str(number_text)]
    freq_dict:dict[str:int] = dict(sorted({k: text.count(k) for k in alphabet}.items(), key=lambda item: item[1], reverse=True))
    sum_all_step_unique_char:int = sum(freq_dict.values())
    freq_dict:dict[str:float] = {k: round(v/sum_all_step_unique_char, 4) for k, v in freq_dict.items()}
    return freq_dict

# Получаем словарь типа буква_шифр: буква
def merge_char_list(lst_alpha: list, lst_text: list) -> dict:
    return dict(map(lambda x, y: (x,y), lst_text, lst_alpha))

# Раскодируем
def get_text(number_text: int, dict_char: dict) -> str:
    text: str = data_text['т'+str(number_text)]
    return ''.join([dict_char[ch] if ch in alphabet else ch for ch in text])

def get_unique_count(dict_alpha: dict) -> list[str]:
    alpha: list[str] = list(dict_alpha.keys())
    alpha_freq: list = list(dict_alpha.values())
    unique_count_freq: list[float] = list({k:v for k, v in Counter(alpha_freq).items() if v>1}.keys()) # [0.0229, 0.0098, 0.0065]
    ltrs_with_same_freq: list[list] = [[k_i for k_i in range(len(alpha_freq)) if alpha_freq[k_i]==v] for v in unique_count_freq]
    alpha_new: list[str] = list()
    last_ind: int = -1
    for i in range(len(ltrs_with_same_freq)):
        min_ind: int = min(ltrs_with_same_freq[i])
        shuffle(ltrs_with_same_freq[i])
        alpha_new.extend(alpha[last_ind + 1:min_ind])
        for x in ltrs_with_same_freq[i]:
            alpha_new.extend(alpha[x])
        last_ind = max(ltrs_with_same_freq[i])
    alpha_new.extend(alpha[max(ltrs_with_same_freq[-1])+1:])
    return alpha_new

def get_decrypt_text(text_number: int) -> str:
    freq_dict:dict[str:float] = get_freq_char(text_number)
    data_char_keys:list[str] = get_unique_count(data_char[text_number - 1])
    # print(data_char_keys)
    merged_dict = merge_char_list(data_char_keys, freq_dict.keys())

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