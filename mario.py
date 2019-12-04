"""
Making Half-Pyramid with given height
"""


height = int(input("Height:  "))
if height > 8 or height < 1:
    print("Enter value between 1 and 8")
else:
    for i in range(height):
        print(" " * (height - i) + ("#" * (i+1)))


