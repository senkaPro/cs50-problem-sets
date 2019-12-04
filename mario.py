"""
Making Half-Pyramid with given height
"""

def get_height():
    height = int(input("Height: "))
    return height

height = get_height()
while height < 1 or height > 8:
    get_height()
for i in range(height):
    print(" " * (height - i) + ("#" * (i+1)))


