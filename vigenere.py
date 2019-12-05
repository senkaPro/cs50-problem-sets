"""
Vigenere cipher - senkaPro
"""

import sys
from cs50 import get_string


def check_arguments():
    '''Function to check for valid arguments'''
    if len(sys.argv) != 2:
        print("Usage: python vigenere.py [KEYWORD]")
        sys.exit(1)
    elif not sys.argv[1].isalpha():
        print("Usage: python vigenere.py [KEYWORD]")
        sys.exit(1)
    return True


def main():

    # validation sys arguments
    check_arguments()

    # prompt for plaintext
    plaintext = get_string("plaintext:")

    # keyword from sys.argv
    kword = sys.argv[1]

    # index counter used for keep index on keyword loop
    j = 0

    # output the ciphertext
    print("ciphertext:", end="")

    # loop throught the plaintext
    for char in plaintext:
        # is the character is not alpha just print it as it is
        if not char.isalpha():
            print(char, end="")
            continue

        # ascii offset variable
        offset = 65 if char.isupper() else 97

        # get char value
        plain = ord(char) - offset
        # get key value
        key = ord(kword[j % len(kword)].upper()) - 65
        # make cipher
        cipher = (plain + key) % 26

        # increase indexer
        j += 1

        # print encrypted char
        print(chr(cipher + offset), end="")
    print()


if __name__ == "__main__":
    main()