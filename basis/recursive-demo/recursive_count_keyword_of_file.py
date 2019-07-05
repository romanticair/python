# Enter a directory and a word or letter, search and return the numbers
# of this word appeared in this directory's files


def search(directory, word, numbers = 0):
    lst = os.listdir(directory)     # 把目录下的文件列出来

    for fileName in lst:           # Is file, count the word
        if os.path.isfile(directory + "\\" + fileName):
            with open(directory + "\\" + fileName, "r", encoding = 'utf-8', errors = 'ignore') as file: # 这一句改动了
                numbers += file.read().split().count(word)  # 这一句改动了
        else:                      # Not a file, recursive, until it's a file
            numbers += search(directory + "\\" + fileName, word)

    # Return the numbers of word
    return numbers

if __name__ == '__main__':
    import os

    # Enter a directory route like  L:\\WeeklyHomeworks\\AllAnswer
    while True:
        directoryName = input("Enter a directory name: ").strip()
        if os.path.isdir(directoryName):
            print("Directory exit, go on ")
            break
        print("Does't exit, Please try again")

    # Execute Function
    try:
        print("end with : ", search(directoryName, 'a'))
    except UnicodeDecodeError:
        pass
