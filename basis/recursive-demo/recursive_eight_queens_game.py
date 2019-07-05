queen = 8 * [-1] #  第几行第几个


def conflict(row, column):
    global queen
    for i in range(1, row + 1):
        if (queen[row - i] == column             # Check if the same column
            or queen[row - i] == column - i      # Check positive line
            or queen[row - i] == column + i):    # Check negative line
            return True
    return False

def queens(n, row):
    global  queen, solutions
    if n == row :       # found
        print(queen)
        queen[-1] = -1  # back a postion
        solutions += 1
        return True
    for column in range(n):     # Try any positions
        queen[row] = column
        if not conflict(row, column) :
            queens(n, row + 1)
        else:
            queen[row] = -1      # row position is't fit, back
    return False

solutions = 0
queens(8, 0)
print(solutions)
