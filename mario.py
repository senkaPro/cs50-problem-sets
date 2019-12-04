"""
Making Half-Pyramid with given height
"""
def get_int():
    imp = input("Height: ")
    if imp.isdigit():
        return int(imp)
    else:
        return False

while True:
    height = get_int()
    if height != False and height > 0 and height <= 8:
        for i in range(height):
            print(" " * (height - i),end="")
            print("#" * (i+ 1))
        break
