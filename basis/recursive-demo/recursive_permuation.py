def displayPermuation(s):
    s1 = ''
    s2 = s
    displayPermuationHelper(s1, s2)

def displayPermuationHelper(s1, s2):
    if len(s2) == 0:    # Base condition
        print(s1)
        return ''
    else:               # Recursion
        for i in range(len(s2)):
            displayPermuationHelper(s1 + s2[i], s2[:i] + s2[len(s2):i:-1])

if __name__ == '__main__':
    print(displayPermuation('abc'))
