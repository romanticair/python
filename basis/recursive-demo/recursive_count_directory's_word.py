import os


def search(directory, word, numbers = 0):
    lst = os.listdir(directory) # 把目录下的文件列出来
    for fileName in lst: # Is file, count the word
        if os.path.isfile(directory + "\\" + fileName):
            with open(directory + "\\" + fileName, "r", encoding = 'utf-8', errors = 'ignore') as file:
                numbers += file.read().count(word)
        else: # Not a file, recursive, until it's a file
            numbers += search(directory + "\\" + fileName, word)

    return numbers

if __name__ == '__main__':
    while True:
        directoryName = input("Enter a directory name: ").strip()
        if os.path.isdir(directoryName):
            print("Directory exit, go on ")
            break
        print("Does't exit, Please try again")

    try :
        print("end with : ", search(directoryName, 'a'))
    except UnicodeDecodeError:
        print("Here's a bug")
