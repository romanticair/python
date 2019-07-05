# Task 4: Fun with Recursion, part 2

def copy(s, n):
    # Takes a string s and an integer n, create and return a string in
    # which n copies of s have been concatenated together.
    # If n is less than or equal to 0, function will return empty string
    if len(s) <= 0 or n <= 0:
        return ''
    test_n = copy(s, n - 1)
    return s + test_n

def double(s):
    # Takes an abitrary string to construct and return the string formed by doubing
    # each character in the string by using recursion
    if len(s) == 0:
        return ''
    test_n = double(s[1:])
    return 2 * s[0] + test_n

def weave(s1, s2):
    # Takes two string s1 and s2, uses recursion to constuct and return a new
    # string that's formed by weaving together the characters in the string s1
    # and s2 to create a single string.
    # If one of the two string is longer than other, then the extra characters
    # will link directly
    if len(s1) and len(s2) == 0:
        return ''
    elif len(s1) == 0:
        return s2
    elif len(s2) == 0:
        return s1
    test_n = weave(s1[1:], s2[1:])
    return s1[0] + s2[0] + test_n

def  find_min(items):
    # Find the minimum from the list of items.
    # For a list strings, the minimum will be the string closest to the start
    # of the alphabet.
    # For a list of numbers, the minimun will be the smallest number.
    if len(items) == 1:
        return items[0]
    if items[0] < items[1]:
        items[1] = items[0]
    else:
        return find_min(items[1:])
    return find_min(items[1:])

def index(elem, seq):
    # Takes an element elem and a sequence seq, find and return the index of the first
    # occurrence of elem in seq
    # If seq is a string, elem will be a single-character string;
    # If seq is a list, elem can be any value.
    if len(seq) == 0:
        return None
    if len(seq) == 1 and elem != seq[0]:
        return None
    if elem == seq[0]:
        return 0
    """
    j = 0                               还有其它方法吗?
    for i in range(len(seq)):   mylen()
        if seq[i] == elem:
            break
        j += 1
        if j == len(seq) - 1:
            return None
        """
    test_n = index(elem, seq[1:])
    return 1 + test_n
