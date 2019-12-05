"""
Bleep program -senkaPro
"""

import sys
from cs50 import get_string


def check_arguments():
    '''Function to check for valid arguments'''
    if len(sys.argv) != 2:
        print("Usage: python bleep.py dictionary")
        sys.exit(1)
    return True


def main():

    # check for correct arguments
    check_arguments()

    # provided file
    file = sys.argv[1]

    # banned words set
    banned_words = set()

    # prompt user for message
    user_msg = get_string("What message would you like to censor?\n")

    # tokenized message
    tokenized_msg = []

    with open(file, 'r') as f:
        for line in f:
            for word in line.split():
                if word not in banned_words:
                    banned_words.add(word.lower())

    for word in user_msg.split():
        if word.lower() not in banned_words:
            tokenized_msg.append(word)
        else:
            token = "*" * len(word)
            tokenized_msg.append(token)

    for word in tokenized_msg:
        print(word, end=" ")

    print()


if __name__ == "__main__":
    main()
