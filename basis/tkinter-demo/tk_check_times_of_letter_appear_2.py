from tkinter import *
from tkinter.filedialog import askopenfilename
# from tkinter.filedialog import asksaveasfilename


class countLetters_solution:
    """
    Count letters' appeared times
    """
    def __init__(self):
        self.Initialize()

    def create(self):
        self.LETTER_LIST = [chr(i) for i in range(97, 97 + 26)]
        self.LETTER_DICT = {}
        for key in self.LETTER_LIST:
            self.LETTER_DICT[key] = 0

    def Initialize(self):
        self.create()
        x = 20
        self.dx = 13
        self.window = Tk()
        self.canvasBar = Canvas(self.window, width = 400, height = 200)
        self.canvasBar.pack()
        for key in self.LETTER_LIST:
            self.canvasBar.create_text(x, 190, text = key)
            x += 14

        frame2 = Frame(self.window)
        frame2.pack()
        Label(frame2, text="Enter a filename: ").pack(side =LEFT)
        self.textInfo = StringVar()
        Entry(frame2, textvariable=self.textInfo, width=20).pack(side = LEFT)
        Button(frame2, text="Browse", command=self.browse_file).pack(side = LEFT)
        Button(frame2, text="Show Result", command=self.show_result).pack()
        self.window.mainloop()

    def browse_file(self):
        filenameforReading = askopenfilename()
        infile = open(filenameforReading, "r")
        self.get_info_to_file(infile)
        infile.close()

    def get_info_to_file(self, infile):
        # count the numbers of each letter in infile
        # and make it beautiful
        eachLetter = infile.read(1)
        while eachLetter != '':
            if eachLetter.isalpha():
                if eachLetter not in self.LETTER_DICT:
                    self.LETTER_DICT[eachLetter] = 1
                else:
                    self.LETTER_DICT[eachLetter] += 1
            eachLetter = infile.read(1)

        # Return a dict including all the letters and it's appeared times

    def show_result(self):
        try :
            if self.textInfo.get().strip() != '':   # except the space character
                fileRutine = self.textInfo.get()
                infile = open(fileRutine, "r")
                self.allInfoDict = self.get_info_to_file(infile)
                infile.close()
        except IOError or FileNotFoundError:
            print("Enter's wrong, please try")
        finally:
            for key in self.LETTER_LIST:
                self.canvasBar.create_rectangle(self.dx, 170 - 10 * self.LETTER_DICT[key],
                                                self.dx + 14, 180, fill = 'red')
                self.dx += 14
        self.create()

if __name__ == '__main__':
    countLetters_solution()
