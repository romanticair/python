times = 0


def main():
    n = eval(input("Enter number of disks: "))
    # Find the solution recursively
    print("The moves are: ")
    moveDisks(n, 'A', 'B', 'C')

# The function for finding the solution to move n disks
# from fromTowe to toTower with auxTower


def moveDisks(n, fromTower, toTower, auxTower):
    global times
    times += 1
    if n == 1:  # Stopping condition
        print("Move disk ", n, "from", fromTower, "to", toTower)
    else:
        moveDisks(n - 1, fromTower, auxTower, toTower)
        print("Move disk ", n, "from", fromTower, "to", toTower)
        moveDisks(n - 1, auxTower, toTower, fromTower)

if __name__ == '__main__':
    main()
    print(times)
