"""
Caesar cipher encoding program - senkaPro
"""

import sys
from cs50 import get_string

if len(sys.argv) != 2:
    print("Usage: python cypher.py [KEY]")
    sys.exit(1)

key = int(sys.argv[1])

if key < 1 or key > 26:
    sys.exit(1)

plaintext = get_string("plaintext: ")

print("plaintext: ",end = '')


for char in plaintext:
    if not char.isalpha():
        print(char, end = '')
        continue

    offset = 65 if char.isupper() else 97

    plain = ord(char) - offset
    cipher = (plain + key) % 26

    print(chr(cipher + offset), end='')

print()