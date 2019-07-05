from tkinter import *
from tkinter.filedialog import askopenfilename
# from tkinter.filedialog import asksaveasfilename


class countLetters_solution:
    """
    Count letters' appeared times
    """
    def __init__(self):
        window = Tk()
        frame1 = Frame(window)
        frame1.grid()

        scrollbar = Scrollbar(frame1)
        scrollbar.pack(side = RIGHT, fill = Y)
        self.text = Text(frame1, width = 50, height = 20,
                         wrap = WORD, yscrollcommand = scrollbar.set)
        self.text.pack()
        scrollbar.config(command = self.text.yview())

        frame2 = Frame(window)
        frame2.grid()
        Label(frame2, text = "Enter a filename: ").grid(row = 1, column = 1)
        self.textInfo = StringVar()
        Entry(frame2, textvariable = self.textInfo, width = 20).grid(row = 1, column = 2)
        Button(frame2, text = "Browse", command = self.browse_file).grid(row = 1, column = 3)
        Button(frame2, text = "Show Result", command = self.show_result).grid(row = 1, column = 4)

        window.mainloop()

    def browse_file(self):
        filenameforReading = askopenfilename()
        infile = open(filenameforReading, "r")
        self.allInfoDict = self.get_info_to_file(infile)
        infile.close()

    def get_info_to_file(self, infile):
        # count the numbers of each letter in infile
        # and make it beautiful
        allInfoDict = {}    # create a dict
        eachLetter = infile.read(1)
        while eachLetter != '':
            if eachLetter.isalpha():
                if eachLetter not in allInfoDict:
                    allInfoDict[eachLetter] = 1
                else:
                    allInfoDict[eachLetter] += 1
                eachLetter = infile.read(1)

        return allInfoDict  # Return a dict including all the letters and it's appeared times

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
            for key in self.allInfoDict:
                if self.allInfoDict[key] < 2:
                    self.text.insert(END, "{}  appears  {}  time\n".format(key, self.allInfoDict[key]))
                else:
                    self.text.insert(END, "{}  appears  {}  times\n".format(key, self.allInfoDict[key]))

        self.allInfoDict.clear()  # clear information after showed

if __name__ == '__main__':
    countLetters_solution()
