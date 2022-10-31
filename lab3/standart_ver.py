CAPACITY = pow(2,64)

def hash(text: str) -> int:
    key = len(text)
    text = list([ord(x) for x in text])
    rez = sum([text[i-1]*i for i in range(1, key+1)])%CAPACITY
    return rez

# def test():
#     count_k = 0
#     word = ''
#     hash_table = []

#     for text_size in range(0, 10):
#         new_char = ''
#         for char_ind in range(1, 1000):
#             new_char = chr(char_ind)
#             if (hash(word + new_char)) in hash_table:
#                 # print(word + new_char, hash(word + new_char))
#                 count_k+=1
#             hash_table.append(hash(word + new_char))
#         word+=new_char
#     return count_k

def main():

    text: list[str] = input('Enter stride: ')
    print(hash(text))
    # print("Кол-во коллизий: ", test())

if __name__ == '__main__':
    main()