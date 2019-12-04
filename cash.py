"""
Cash.py - senkaPro
"""


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
    # Get input from the user
    change = get_float()

    # This if statement check if user provided us with float
    if change != False and change > 0:

        # We change the coins user provided into pennies
        coins = round(change * 100)

        # change_coins keep track of how many coins we return
        change_coins = coins // quarters

        # coins_left keep track of the remained pennies
        coins_left = coins % quarters

        # if we can return dimes we increase change_coins
        if coins_left >= dimes:
            change_coins += coins_left // dimes
        # We check coins left after returning dimes
        coins_left %= dimes

        # We check nickels to return
        if coins_left >= nickels:
            change_coins += coins_left // nickels

        # We check coins left after returning nickels
        coins_left %= nickels

        # Since only pennies are left we add them to the change_coins mean we returned pennies also
        change_coins += coins_left
        print(change_coins)
        break
