import os

# os.path.getsize(filename) return the size of filename
# os.listdir(directory) return all files under the directory

def main():
    # Prompt the user to enter a directory or a file
    path = input("Enter a directory or a file: ").strip()

    # Dispaly the size
    try:
        print(getSize(path), "bytes")
    except:
        print("Directory or file does not exist")

def getSize(path):
    size = 0
    if not os.path.isfile(path):
        lst = os.listdir(path)   # All files and subdirectories
        for subdirectory in lst:
            print(subdirectory)
            size += getSize(path + "\\" + subdirectory)
    else:   # Base case, it is a file
        print(path)
        size += os.path.getsize(path)       # Accumulate file size

    return size

if __name__ == '__main__':
    main()
