########################
# Assignment 2, Task 2 #
########################

def opposite(number):
    # return the opposite number
    return - 1 * number

# 2 -> -2
# print(opposite(-5))

def cube(number):
    # return the cube of number
    return number ** 3

# 2 -> 8
# print(cube(-5))

def slope(x1, y1, x2, y2):
    # return the slopes of the line formed by two points
    return (y2 - y1) / (x2 - x1)

# line between points (2, 3) and (4, 7)
# print(slope(2, 3, 4, 7))

def make_change(cents):
    # return list which include four minimize coins
    quarters = cents // 25
    dimes = cents % 25 // 10
    nickles = cents % 25 % 10 // 5
    pennies = cents % 25 % 10 % 5
    return [quarters, dimes, nickles, pennies]

# 347cents -> 13 quarters, 2 dimes, 0 nickles, 2 pennies
# print(make_change(347))
# print(make_change(84))
