"""
Caesar cipher encoding program - senkaPro
"""

import sys
from cs50 import get_string

# check for correct arguments
if len(sys.argv) != 2:
    print("Usage: python cypher.py [KEY]")
    sys.exit(1)

# set key as an int
key = int(sys.argv[1])

# prompt for plaintext
plaintext = get_string("plaintext: ")

# start printing ciphertext
print("ciphertext: ", end="")

# loop throught plaintext and change it to ascii chars
for char in plaintext:
    # if char is not alphanumeric just print it as it is
    if not char.isalpha():
        print(char, end='')
        continue

    # set ascii offset
    offset = 65 if char.isupper() else 97

    # calculate value for ascii char
    plain = ord(char) - offset

    # offset the cipher for the given key
    cipher = (plain + key) % 26

    # print out encrypted char
    print(chr(cipher + offset), end='')

# end with new line
print()