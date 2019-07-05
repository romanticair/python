def recursiveBinarySearch(lst, key):
    low = 0
    high = len(lst) - 1
    return recursiveBinarySearchHelper(lst, key, low, high)


def recursiveBinarySearchHelper(lst, key, low, high):
    if low > high:  # The list has been exhausted without a match
        return False

    mid = (low + high) // 2
    if lst[mid] == key:
        return mid
    elif lst[mid] < key:
        return recursiveBinarySearchHelper(lst, key, mid + 1, high)
    else:
        return recursiveBinarySearchHelper(lst, key, low, mid - 1)

if __name__ == '__main__':
    lst = [3, 5, 6, 8, 9, 12, 34, 36]
    print(recursiveBinarySearch(lst, 12))
    print(recursiveBinarySearch(lst, 4))