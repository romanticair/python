"""
1.二分法查找(有序列表)
2.冒泡排序
3.鸡尾酒排序
4.选择排序
5.插入排序
6.归并排序
7.快速排序
8.堆排序
9.希尔排序 -- 未完成
10.基数排序 -- 未完成
可参照 http://python.jobbole.com/82270/
"""


def binary_search(arr, key):
    """二分法查找(有序列表) return index"""
    low = 0
    high = len(arr) - 1
    while low <= high:
        half = (low + high) // 2
        if arr[half] == key:
            return half
        elif key < arr[half]:
            high = half - 1
        else:
            low = half + 1
    else:
        return "%d not find in the arr." % key


def bubble_sort(arr, reverse=False):
    """冒泡排序"""
    length = len(arr)
    for i in range(0, length):
        for j in range(0, length - i - 1):
            if reverse and arr[j] < arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
            elif not reverse and arr[j] > arr[j+1]:
                arr[j+1], arr[j] = arr[j], arr[j+1]

    return arr


def cocktail_sort(arr):
    """
    鸡尾酒排序

    在与冒泡排序不同的是，这儿一次顺序找最大，一次逆序找最小，
    即往后冒最大的泡，往前压最小的泡。
    """
    length = len(arr)
    for i in range(0, length//2):
        # -> 找 max value 顺序
        index = i
        last_index = length - i - 1
        max_value = arr[i]
        for j, val in enumerate(arr[i: last_index + 1]):
            if val > max_value:
                index = j + i
                max_value = val
        if index != i:
            arr[index] = arr[last_index]
            arr[last_index] = max_value
        
        # <- 找 min value 逆序
        index = i
        min_value = arr[last_index]
        for j in range(last_index - 1, i - 1, -1):
            if arr[j] < min_value:
                index = j
                min_value = arr[j]
        if index != i:
            arr[index] = arr[i]
            arr[i] = min_value
        
    return arr                


def select_sort(arr, reverse=False):
    """选择排序,升序"""
    length = len(arr)
    for i in range(length):
        pre_index = i
        for j in range(i + 1, length):
            if not reverse and arr[pre_index] > arr[j]:
                i = j
            elif reverse and arr[pre_index] < arr[j]:
                i = j
        if pre_index != i:
            arr[i], arr[pre_index] = arr[pre_index], arr[i]

    return arr


def insert_sort(arr, reverse=False):
    """插入排序

    插入排序的基本操作就是将一个数据插入到已经排好序的有序数据中，从而得到一个新的、个数加一的有序数据，
    算法适用于少量数据的排序，时间复杂度为O(n^2)。是稳定的排序方法。插入算法把要排序的数组分成两部分：
    第一部分包含了这个数组的所有元素，但将最后一个元素除外（让数组多一个空间才有插入的位置），而第二部
    分就只包含这一个元素（即待插入元素）。在第一部分排序完成后，再将这个最后元素插入到已排好序的第一部
    分中"""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0:
            if not reverse and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            elif reverse and arr[j] < key:
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break
        arr[j + 1] = key
    
    return arr

        
def merge_sort(arr):
    """
    归并排序
    
    To implement the merge sort algorithm on a arr
    of values. The result of this function call will
    be to sort the arr.
    """
    if len(arr) <= 1:
        return arr

    left = arr[: len(arr)//2]
    right = arr[len(arr)//2:]
    arr_l = merge_sort(left)            # 切左边直到成单个
    arr_r = merge_sort(right)           # 切右边直到成单个
    return combine_arr(arr_l, arr_r)   # 左右combine, 出栈
    

def combine_arr(left, right):
    """
    Assumes that each arr is already in sorted order
    Combine two arr into one arr in sequence
    """
    if len(left) == 0:
        return right
    if len(right) == 0:
        return left

    if left[0] > right[0]:
        return [right[0]] + combine_arr(left[:], right[1:])
    elif left[0] <= right[0]:
        return [left[0]] + combine_arr(left[1:], right[:])


def quick_sort(arr, left, right):
    """
    快速排序法

    这里将 left 索引所在位置的值设定为基准值，left, right 两哨兵在逼近检查且交换值过程中不断靠拢，使大于基准值 pivot 的
    数分到右侧部分，小于它的数分到左侧部分，每次检查完基准值都与临界值交换，此时基准值将序列分为两序列
    (左序列的值都小于基准值，右序列的值都大于基准值)，在已分好的各序列继续递归直至全部成序。
    """
    if left >= right:
        return
    pivot = arr[left]
    low = left
    high = right
    while left < right:
        while arr[right] >= pivot and left < right:
            right -= 1
        while arr[left] <= pivot and left < right:
            left += 1
        if left < right:
            # swap
            arr[left], arr[right] = arr[right], arr[left]

    # divided into two parts, swap pivot as median value
    arr[low], arr[left] = arr[left], pivot
    quick_sort(arr, low, left - 1)
    quick_sort(arr, left + 1, high)
    return arr


def max_heapify(heap,heapSize,root):
    """
    调整列表中的元素并保证以root为根的堆是一个大根堆
    
    给定某个节点的下标root，这个节点的父节点、左子节点、右子节点的下标都可以被计算出来。
    父节点：(root-1)//2
    左子节点：2*root + 1
    右子节点：2*root + 2  即：左子节点 + 1
    """
    left = 2 * root + 1
    right = left + 1
    larger = root
    if left < heapSize and heap[larger] < heap[left]:
        larger = left
    if right < heapSize and heap[larger] < heap[right]:
        larger = right
    # 如果做了堆调整则larger的值等于左节点或者右节点的值，这个时候做堆调整操作
    if larger != root:
        heap[larger], heap[root] = heap[root], heap[larger]
        # 递归的对子树做调整
        max_heapify(heap, heapSize, larger)
 
 
def build_max_heap(heap):
    """
    建立大根堆
    
    构造一个堆，将堆中所有数据重新排序
    """
    heapSize = len(heap)
    # 自底向上建堆
    for i in range((heapSize - 2)//2, -1, -1):
        max_heapify(heap, heapSize, i)

        
def heap_sort(heap):
    """
    原文链接，https://blog.csdn.net/june_young_fan/article/details/82014081
    学习了，感谢！
    
    将根节点取出与最后一位做对调，对前面len-1个节点继续进行堆调整过程。
    调整后列表的第一个元素就是这个列表中最大的元素，将其与最后一个元素交换，然后将剩余的列表再递归的调整为最大堆
    """
    build_max_heap(heap)
    for i in range(len(heap)-1, -1, -1):
        heap[0], heap[i] = heap[i], heap[0]
        max_heapify(heap, i, 0)
        
    return heap
 
array1 = [3, 8, 7, 4, 6, 5, 1]
array2 = [2, 5, 84, 7, 46, 7, 94, 3]
array3 = [1, 2, 4, 6, 7, 8, 9, 10, 12]
array4 = [1, 7, 5, 4, 3, 8, 9, 2, 6]

# 二分法查找(有序列表)测试
print("binary_search test:")
print(binary_search(array3, 2))
print(binary_search(array3, 5))
print(binary_search(array3, 12))

# 冒泡排序测试
print("bubble_sort test:")
print(bubble_sort(array1, True))
print(bubble_sort(array2, True))
print(bubble_sort(array1))
print(bubble_sort(array2))

# 鸡尾酒排序测试
print("cocktail_sort test:")
print(cocktail_sort(array1))
print(cocktail_sort(array2))
print(cocktail_sort(array4))

# 选择排序测试
print("select_sort test:")
print(select_sort(array1, True))
print(select_sort(array2, True))
print(select_sort(array1))
print(select_sort(array2))

# 插入排序测试
print("insert_sort test:")
print(insert_sort(array1, True))
print(insert_sort(array2, True))
print(insert_sort(array1))
print(insert_sort(array2))

# 归并排序测试
print("merge_sort test:")
print(merge_sort(array1))
print(merge_sort(array2))

# 快速排序测试
print("quick_sort test:")
print(quick_sort(array1, 0, len(array1) - 1))
print(quick_sort(array2, 0, len(array1) - 1))
print(quick_sort(array4, 0, len(array1) - 1))

# 堆排序测试
print("heap_sort test:")
print(heap_sort(array1))
print(heap_sort(array2))
print(heap_sort(array3))
