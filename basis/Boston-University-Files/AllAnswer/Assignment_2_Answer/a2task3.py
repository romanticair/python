# Task 3: Fun with recursion, part I

def mylen(s):
    """ returns the length of the sequence s
        input: s is a sequence (a string or list)
    """
    if s == '' or s == []:
        return 0
    else:
        len_rest = mylen(s[1:])
        return 1 + len_rest

def mult(n, m):
    # takes two integers n and m as inputs and uses recursion to
    # compute the sum of n plus m by not use operator(*) and
    # return the product of those intergers
    if n == 0:
        return 0
    if n < 0:
        return  - mult(- n, m)
    mult_test = mult(n - 1, m)
    return m + mult_test

def dot(list1, list2):
    # Takes two lists of numbers, compute and return the sum of the
    # product of the elements in the same positons in two lists.
    # But if two lists' length is't the same, dot() will return 0.0
    if mylen(list1) != mylen(list2):
        return 0.0
    if mylen(list1) == 0:
        return 0
    dot_test = dot(list1[1:], list2[1:])
    return 1.0 * list1[0] * list2[0] + dot_test

def letter_score(letter):
    # Takes a lowercase letter as input and returns the value of
    # that letter as a scrabble tile  (a -> 26, b -> 25,... z -> 1)
    # But if letter is't a lowercase letter, or 'a' ->  'b',function will return 0
    assert (len(letter) == 1)
    scoresList = ['aeilorstun', 'dg', 'bcmp', 'fhvwy', 'k', '', '', 'jx', '', 'qz']
    i = 1
    for j in scoresList:
        if letter in j:
            return i
        i += 1
    return 0



def num_vowels(s):
    """ returns the number of vowels in the string s
        input: s is a string of 0 or more lowercase letters
    """
    if s == '':
        return 0
    else:
        num_in_rest = num_vowels(s[1:])
        if s[0] in 'aeiou':
            return 1 + num_in_rest
        else:
            return 0 + num_in_rest

def scrabble_score(word):
    # Similar to letter_score, the difference's the word is a string which
    # only admit lowercase letters and uses recursion to compute and return
    # the sum of score of this word, each letter has its vowel score as its value
    # help by letter_score()
    if len(word) == 0:
        return 0
    test_n = scrabble_score(word[1:])
    return  letter_score(word[0]) + test_n


def test():
    # test function for the function above
    test1 = mult(6, 7)
    print("The first test returns: ", test1)
    test2 = dot([2, 5], [10, 2])
    print("The second test returns: ", test2)
    test3 = letter_score('q')
    print("The third test returns: ", test3)
    test4 = scrabble_score('python')
    print("The fourth test returns: ", test4)


