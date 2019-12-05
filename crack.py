"""
Crack program - senkaPro
"""
import crypt
import sys
from cs50 import get_string


def check_arguments():
    '''Function to check for valid arguments'''
    if len(sys.argv) != 2:
        print("Usage: python crack.py [HASH]")
        sys.exit(1)
    return True


def main():
    # check for user arguments
    check_arguments()

    # get hash value
    hash = sys.argv[1]

    # salt the first 2 chars of hash
    salt = hash[0:2]

    # letters to include in the cracking
    letters = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # loop to max of 5 chars in password and compare hash with our crypt hash
    for i in letters:
        for j in letters:
            for k in letters:
                for l in letters:
                    for m in letters[1:]:
                        password = f"{m}{l}{k}{j}{i}".strip()

                        # if password found print output
                        if crypt.crypt(password, salt) == hash:
                            print(password)
                            sys.exit(0)


if __name__ == "__main__":
    main()