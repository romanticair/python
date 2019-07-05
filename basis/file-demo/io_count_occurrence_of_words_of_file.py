def main():
    # Prompt the user to enter a file
    filename = input("Enter a filename: ").strip()
    infile = open(filename, "r")

    wordCounts = {} # Create a empty dictionary to count words
    for line in infile:     # read by line
        processLine(line.lower(), wordCounts)

    print(wordCounts)
    pairs = list(wordCounts.items())        # Get pairs from the dictionary
    items = [[x, y] for (y, x) in pairs]    # Reverse pairs in the list
    items.sort()
    for i in range(len(items) - 1, -1, -1):
        print(items[i][1] + "\t" + str(items[i][0]))
    infile.close()

# Count each word in the line
def processLine(line, wordCounts):
    line = replacePunctuations(line)    # Replace punctuation with space
    words = line.split()    # Get words from each line
    for word in words:
        if word in wordCounts:
            wordCounts[word] += 1
        else:
            wordCounts[word] = 1

# Replace punctuation in the line with a space
def replacePunctuations(line):
    for ch in line:
        if ch in "`@#$%!^&*()?_=+-'|\/;:.,><[]{}\"":
            line = line.replace(ch, " ")

    return line

if __name__ == '__main__':
    main()