def combine_lists(left, right):
    # Assumes that each list is already in sorted order
    # Combine two lists into one list in sequence
    if len(left) == 0:
        return right
    if len(right) == 0:
        return left

    if left[0] > right[0]:
        return [right[0]] + combine_lists(left[:], right[1:])
    elif left[0] <= right[0]:
        return [left[0]] + combine_lists(left[1:], right[:])

def merge_sort(values):
    # To implement the merge sort algorithm on a list
    # of values. The result of this function call will
    # be to sort the list.
    if len(values) <= 1:
        return values

    left = values[: len(values) // 2]
    right = values[len(values) // 2:]
    list_l = merge_sort(left)        # 切左边直到成单个
    list_r = merge_sort(right)       # 切右边直到成单个
    return combine_lists(list_l, list_r)    # 左右combine,出栈

# print(merge_sort([9, 2, 4, 6, 14, 8, 7, 12]))