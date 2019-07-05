# Sum columns in a text file separated by commas

filename = 'data.txt'  # 3, 4, 5
sums = {}              # 5. 3. 9

for line in open(filename):
    cols = line.split(',')
    nums = [int(col) for col in cols]
    for (ix, num) in enumerate(nums):
        sums[ix] = nums.get(ix, 0) + num

for key in sorted(sums):
    print(key, ' = ', sums[key])