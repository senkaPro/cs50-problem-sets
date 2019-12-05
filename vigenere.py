"""
Vigenere cipher - senkaPro
"""

import sys
from cs50 import get_string


def check_arguments():
    if len(sys.argv) != 2:
        print("Usage: python vigenere.py [KEYWORD]")
        sys.exit(1)
    elif not sys.argv[1].isalpha():
        print("Usage: python vigenere.py [KEYWORD]")
        sys.exit(1)
    return True


def main():

    check_arguments()

    plaintext = get_string("plaintext:")
    kword = sys.argv[1]
    j = 0

    print("ciphertext:", end="")

    for char in plaintext:
        if not char.isalpha():
            print(char, end="")
            continue

        offset = 65 if char.isupper() else 97

        plain = ord(char) - offset
        key = ord(kword[j % len(kword)].upper()) - 65
        cipher = (plain + key) % 26

        j += 1

        print(chr(cipher + offset), end="")
    print()



if __name__ == "__main__":
    main()