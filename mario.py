"""
Making double-Pyramid with given height
"""


def get_int():
    """Function to get integer and return false otherwise"""
    imp = input("Height: ")
    if imp.isdigit():
        return int(imp)
    else:
        return False


# Looping till we get number between 1 and 8 and than drawing the
while True:
    height = get_int()
    if height != False and height > 0 and height <= 8:
        for i in range(1, height+1):
            print(" " * (height - i), end="")
            print("#" * i + "  " + "#" * i)      # Here we added 2 spaces and revert the pyramid
        break