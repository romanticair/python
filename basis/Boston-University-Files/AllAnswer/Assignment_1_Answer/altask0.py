########################
# Assignment 1, Task 1 #
########################
pi = [3, 1, 4, 1, 5, 9]
e = [2, 7, 1]
# First half of Puzzle:
# Creating the list [ whatNumber, whatNumber ] from pi and e

answer0 = [e[0]] + pi[-2 :]
# print(answer0)

answer1 = e[0 : 2]
# print(answer1)

answer2 = pi[-2 : : -2]
# print(answer2)

answer3 = pi[0 : 5 : 4] + [e[1]]
# print(answer3)

answer4 = e[-1 : -4 : -2] + pi[0 : 5 : 2]
# print(answer4)

b = 'boston'
u = 'university'
t = 'terriers'
# Second half of Puzzle:
# Creating the str [ whatString, whatString ] from b and u and t

answer5 = b[0 : 3] + u[-4 : : 3]
# print(answer5)

answer6 = u[0 : 7] + u[4]
# print(answer6)

answer7 = t[2] + b[1 : 4] + u[4 : 6]
# print(answer7)

answer8 = b[0 : 2] + u[-3 : -5 : -1] + t[0 : 3] + b[1] + u[0 : 7 : 6]    # 8 ops ?
# print(answer8)

answer9 = (u[-1] + t[-1 : -4 : -2]) * 3
# print(answer9)

answer10 = t[0 : 5 : 2] + b[2 : 4]
# print(answer10)


