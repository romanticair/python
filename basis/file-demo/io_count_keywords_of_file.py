
import os.path
import sys

# 读文件keyWords出现次数
def main1():
    keyWords = {"and", "as", "assert", "break", "class",
                "continue", "def", "del", "elif", "else",
                "except", "False", "finally", "for", "lambda",
                "global", "if", "import", "in", "is", "from",
                "None", "nonlocal", "not", "or", "pass", "raise",
                "return", "True", "try", "while", "with", "yield"}
    filename = input("Enter a Python source code filename: ").strip()

    if not os.path.isfile(filename):
        print("File", filename, "does not exist")
        sys.exit()

    infile = open(filename, "r")
    text = infile.read().split()    # split word by space

    count = 0
    for word in text:
        if word in keyWords:
            count += 1
    infile.close()
    print("The number of Keywords in", filename, "is", count)

def main2():
    # The keywords in python
    # Function is use for check a source file of how many keywords in
    keyWords = {"and", "as", "assert", "break", "class",
                "continue", "def", "del", "elif", "else",
                "except", "False", "finally", "for", "lambda",
                "global", "if", "import", "in", "is", "from",
                "None", "nonlocal", "not", "or", "pass", "raise",
                "return", "True", "try", "while", "with", "yield"}
    Key = {}
    filename = input("Enter a Python source code filename: ").strip()
    if not os.path.isfile(filename):
        print("File", filename, "does not exist")
        sys.exit()

    infile = open(filename, "r")
    text = infile.read().split()  # split word by space
    for word in text:
        if word in keyWords:
            if word not in Key:
                Key[word] = 1
            else:
                Key[word] += 1
    infile.close()
    for i in Key:
        print("{} -> {} times".format(i, Key[i]))

if __name__ == '__main__':
    main1()
    main2()