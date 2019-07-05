def copyDict(old):
    new = {}
    for key in old.keys():
        new[key] = old[key]
    return new


def addDict(d1, d2):
    new = {}
    for key in d1.keys():
        new[key] = d1[key]
    for key in d2.keys():
        new[key] = d2[key]

    return new

d = {1: 1, 2: 2}
e = copyDict(d)
d[2] = '?'
print(d)
print(e)

x = {1: 1}
y = {2: 2}
z = addDict(x, y)
print(z)
