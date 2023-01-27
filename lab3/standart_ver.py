CAPACITY = pow(2,64)

def hash(text: str) -> int:
    key = len(text)
    text = list([ord(x) for x in text])
    rez = sum([text[i-1]*i for i in range(1, key+1)]) % CAPACITY
    return rez

def main():

    text: list[str] = input('Enter stride: ')
    print(hash(text))

if __name__ == '__main__':
    main()