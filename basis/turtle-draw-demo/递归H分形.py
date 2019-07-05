import turtle


def run(n, d):
    # 递归创建 H 分形
    if n == -1:
        return
    else:
        turtle.setheading(0)
        for angle in (0, 90, 1, 180, 0, 2, 180, 90, 0, -90, 1, 180, 0, 2):
            if angle == 1:
                run(n - 1, d / 2)
                turtle.setheading(90)
                continue
            if angle == 2:
                run(n - 1, d / 2)
                turtle.setheading(270)
                continue
            turtle.lt(angle)
            turtle.forward(d / 2)
    turtle.bk(d / 2)
    turtle.lt(90)
    turtle.forward(d / 2)

if __name__ == '__main__':
    run(2, 200)
    turtle.mainloop()
