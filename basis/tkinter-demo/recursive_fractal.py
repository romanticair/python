from tkinter import *
COUNT_LIMIT = 60


class Draw:
    def __init__(self):
        window = Tk()
        self.canvas = Canvas(window)
        self.canvas.grid()
        Button(window,text = "Dispaly1", command = self.paint1).grid()
        Button(window,text = "Dispaly2", command = self.paint2).grid()
        window.mainloop()

    def paint1(self):
        x = - 2.0
        while x < 2.0:
            y = - 2.0
            while y < 2.0:
                c = self.count1(complex(x, y))
                if c == COUNT_LIMIT:
                    color = "red"
                else:
                    color = "blue"
                self.canvas.create_rectangle(x * 100 + 300, y * 100 + 150,
                                        x * 100 + 200 + 5, y * 100 + 200 + 5, fill = color)
                y += 0.05
            x += 0.05

    def paint2(self):
        x = - 2.0
        while x < 2.0:
            y = - 2.0
            while y < 2.0:
                z = self.count2(complex(x, y))
                if z == COUNT_LIMIT:
                    color = "red"
                else:
                    color = "blue"
                self.canvas.create_rectangle(x * 100 + 300, y * 100 + 150,
                                        x * 100 + 200 + 5, y * 100 + 200 + 5, fill = color)
                y += 0.05
            x += 0.05

    def count1(self, c):
        z = complex(0, 0)
        for i in range(COUNT_LIMIT):
            z = z * z + c
            if abs(z) > 2: return i
        return COUNT_LIMIT

    def count2(self, z):
        c = complex(- 0.3, 0.6)
        for i in range(COUNT_LIMIT):
            z = z * z + c
            if abs(z) > 2: return i
        return COUNT_LIMIT

Draw()
