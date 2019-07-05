import turtle


def tree(n, d):
    # left -> right
    if n == 0:
        turtle.forward(d)
    else:
        turtle.forward(d)
        for angle in (30, - 60):
            turtle.lt(angle)
            tree(n - 1, d / 2)
            turtle.bk(d / 2)

        turtle.lt(30)

turtle.lt(90)
tree(9, 150)
turtle.mainloop()
