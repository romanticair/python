import turtle


def polygon_by_triangle():
    # 多三角构成的多边形
    turtle.speed(10)
    turtle.lt(60)
    for i in range(6):
        turtle.lt(60)
        turtle.forward(50)
        turtle.lt(90)
        turtle.forward(86.6025404)
        turtle.lt(150)
        turtle.forward(100)
        turtle.lt(120)
        turtle.forward(50)


def international_game():
    # 国际象棋盘
    turtle.speed(10)
    turtle.hideturtle()
    for h in range(1,11):
        turtle.penup()
        turtle.goto(-100,120 - h * 20)
        turtle.pendown()
        if h % 2 !=0:
            for i in range(1,11):
                turtle.setheading(-45)
                if i % 2 != 0:
                    turtle.fillcolor('white')
                else :
                    turtle.fillcolor('black')
                turtle.begin_fill()
                turtle.circle(14.1421356237,steps = 4)
                turtle.end_fill()
                turtle.penup()
                turtle.goto(-100 + i * 20 , 120 - h * 20)
                turtle.pendown()
        else :
            for i in range(1,11):
                turtle.setheading(-45)
                if i % 2 == 0:
                    turtle.fillcolor('white')
                else :
                    turtle.fillcolor('black')
                turtle.begin_fill()
                turtle.circle(14.1421356237,steps = 4)
                turtle.end_fill()
                turtle.penup()
                turtle.goto(-100 + i * 20 , 120 - h * 20)
                turtle.pendown()

if __name__ == '__main__':
    polygon_by_triangle()
    international_game()
