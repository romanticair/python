import os

# enter a directory , show the files number
def main():
    path = input("Enter a directory or a file: ").strip()
    try:
        getFiles(path)
    except KeyError or IOError:
        print("Directory or file does not exit")

def getFiles(path):
    if not os.path.isfile(path):    # if it's directory
        lst = os.listdir(path)
        for lst_i in lst:
             getFiles(path + "\\" + lst_i)    # enter all the file to judge
    else:                           # if it's file, print
        print(path)
        return ''

if __name__ == '__main__':
    main()
