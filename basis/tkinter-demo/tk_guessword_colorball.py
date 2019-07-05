import random
from tkinter import *
from random import randint


def guess_words():
    # 猜单词游戏
    words = ["write", "that", "program","happy", "angry", "comfortable"]
    tags = 'y'
    wrong = 0
    right = 0
    while tags == 'y' or tags == 'Y':
        string = words[random.randint(0, len(words) - 1)]   # 随机抽取单词
        secret = ['*'] * len(string)    #  字体长度，未答前全为 *******
        secretString = str()
        for i in range(len(string)):
            secretString += secret[i]

        while right < len(string):
            vowel = input("(Guess) Enter a letter in word " + "{} > ".format(secretString))
            # 若已存在
            if len(vowel) == 1 and (vowel in secret):
                print("{} is already in the word".format(vowel))
                continue
            # 如果猜中里面包含的单词，则显示
            if len(vowel) == 1 and (vowel in string):
                # 显示已答对的
                secretString = str()
                for i in range(len(string)):
                    if string[i] == vowel:
                        secret[i] = string[i]
                        right += 1
                    secretString += secret[i]
            else:
                print("{} is not in the word".format(vowel))
                wrong += 1
        print("The word is {}. You missed {} time".format(string, wrong))
        tags = input('Do you want to guess another word ? Enter y or n >').strip()


class Vowels:
    # 图形化(长柱型)随机字母统计
    def __init__(self):
        window = Tk()
        distance = 10
        self.x = 20
        self.y = 190
        self.bar = Canvas(window, width = 300, height = 200)
        self.bar.pack()
        Button(text = "Display Histogram", command = self.thousandRand).pack(side = BOTTOM)
        for i in range(0, 26):
            self.bar.create_text(self.x + i * distance, self.y, text = "{}".format(chr(97 + i)))
        window.mainloop()

    def thousandRand(self):
        words = [0] * 26
        y = 182
        x = 15
        dx = 10
        self.bar.delete('rectangle')
        for i in range(1000):
            theVowel = random.randint(0, 25)
            words[theVowel] += 1
        for i in range(26):
            self.bar.create_rectangle(x + i * dx, words[i],
                                      x + (i + 1) * dx, y)


def getRandomColor():
    # Return a random color string in the form #RRGGBB
    color = '#'
    for i in range(6):
        color += toHexChar(randint(0,15))
    return color


def toHexChar(hexValue):
    if 0 <= hexValue <= 9:
        return chr(hexValue + ord('0'))
    else:
        return chr(hexValue -10 + ord('A'))


class Ball:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dx = 2
        self.dy = 2
        self.radius = 3
        self.color = getRandomColor()


class BounceBalls:
    # 多彩小球
    def __init__(self):
        self.ballList = []  # Create a list for balls
        window = Tk()
        window.title("Bouncing Balls")
        self.width = 350
        self.height = 150
        self.canvas = Canvas(window, bg ="white",
                             width = self.width, height = self.height)
        self.canvas.pack()
        frame = Frame(window)
        frame.pack()
        btStop = Button(frame, text = "Stop",command = self.stop)
        btStop.pack(side = LEFT)
        btResume = Button(frame, text = "Resume", command = self.resume)
        btResume.pack(side = LEFT)
        btAdd = Button(frame, text ="+",command = self.add)
        btAdd.pack(side = LEFT)
        btRemove = Button(frame, text ="-", command = self.remove)
        btRemove.pack(side = LEFT)
        self.sleepTime = 100
        self.isStopped = False
        self.animate()
        window.mainloop()

    def stop(self):
        self.isStopped = True

    def resume(self):
        self.isStopped = False
        self.animate()

    def add(self):
        self.ballList.append(Ball())

    def remove(self):
        self.ballList.pop()

    def animate(self):
        while not self.isStopped:
            self.canvas.after(self.sleepTime)
            self.canvas.update()
            self.canvas.delete("ball")
            for ball in self.ballList:
                self.redisplayBall(ball)

    def redisplayBall(self, ball):
        if ball.x > self.width or ball.x < 0:
            ball.dx = -ball.dx
        if ball.y > self.height or ball.y < 0:
            ball.dy = -ball.dy

        ball.x += ball.dx
        ball.y += ball.dy
        self.canvas.create_oval(ball.x - ball.radius,
                                ball.y - ball.radius, ball.x + ball.radius,
                                ball.y + ball.radius, fill = ball.color,
                                tags = "ball")

if __name__ == '__main__':
    guess_words()
    Vowels()
    BounceBalls()
