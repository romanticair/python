import turtle
distance = 300


def ice(n, distance):
    # 给定一直线线段，把它等分三段，加入一个等边三角形，以三段的中间一段为底对齐，
    # 再去除该段线段。然后，对每个新线段重复进行上述步骤，就能形成科赫曲线：
    if n == 0 :
        turtle.forward(distance)
        return
    else:
        for angle in (60, -120, 60, 0):
            ice(n - 1, distance / 3)
            # print(angle)
            turtle.lt(angle)  # n = 1, 在1/3处画一个边长为1/3的等边三角形


def iceFlowers(n, distance):
    # 如果画 3 条科赫曲线，每次旋转 120 度，就能得到科赫雪花
    for i in range(3):
        ice(n, distance)
        turtle.rt(120)

iceFlowers(3, 200)
turtle.mainloop()


def koch(t, n):
    """Draws a koch curve with length n."""
    if n < 10:
        t.fd(n)
        return
    m = n/3
    koch(t, m)
    t.lt(60)
    koch(t, m)
    t.rt(120)
    koch(t, m)
    t.lt(60)
    koch(t, m)


def snowflake(t, n):
    """Draws a snowflake (a triangle with a Koch curve for each side)."""
    for i in range(3):
        koch(t, n)
        t.rt(120)

# bob = turtle.Turtle()
# bob.pu()
# bob.goto(-150, 90)
# bob.pd()
# snowflake(bob, 300)
