"""
Cash.py - senkaPro
"""
import math

def get_float():
    """Function to get float and return false otherwise"""
    imp = input("Change owed:  ")
    try:
        return float(imp)
    except:
        return False


quarters = 25
dimes = 10
nickels = 5
pennies = 1

while True:
    change = get_float()
    if change != False and change > 0:
        coins = math.floor(change * 100)
        change_coins = coins / quarters
        coins_left = coins % quarters
        if coins_left >= dimes: change_coins += coins_left / dimes
        coins_left %= dimes
        if coins_left >= nickels: change_coins += coins_left / nickels
        coins_left %= nickels
        change_coins += coins_left
        print(change_coins)
        break
