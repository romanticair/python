import turtle


def binTriangle(n, d):
    if n == -1:
        pass
    else:
        for angle in (120, 120, 120):
            binTriangle(n - 1, d / 2)
            turtle.forward(d)
            turtle.lt(angle)

binTriangle(3, 200)
turtle.mainloop()
