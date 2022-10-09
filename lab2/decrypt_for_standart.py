from data import *

# Инициализируем алфавит
a = ord('а')
alphabet: str = ''.join([chr(i) for i in range(a,a+6)] + [chr(a+33)] + [chr(i) for i in range(a+6,a+32)])

def decrypt(text, offset):
    return ''.join([alphabet[abs(alphabet.index(x) + offset) % len(alphabet)] if x in alphabet else x for x in text])

def main():
    # for i in range(1, len(alphabet)):
    #     print(decrypt(data['т5'], i))

    # print(len(alphabet))

    # Сохраняем найденные ключи
    data_key: dict = {"т1": 3,
                      "т2": 7,
                      "т3": -4, #29
                      "т4": 29, #-4
                      "т5": 19,
                      "т6": 21,
                      "т7": 18,
                      "т8": 22,
                      "т9": 22,
                      "т10": 13}
    for k, v in data_key.items():
        print(f"{k}: {decrypt(data_text_standart[k], v)}")


if __name__=="__main__":
  main()