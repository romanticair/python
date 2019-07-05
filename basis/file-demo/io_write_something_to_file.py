from random import randint

def main():
    # Write 10 random number to file
    outfile = open("Numbers.txt", "w")
    for i in range(10):
        outfile.write(str(randint(0, 9)) + "")
    outfile.close()

    # Open file for read data
    infile = open("Numbers.txt", "r")
    s = infile.read()
    numbers = [eval(x) for x in s.split()]
    for number in numbers:
        print(number, end = "")
    infile.close()

if __name__ == '__main__':
    main()
	