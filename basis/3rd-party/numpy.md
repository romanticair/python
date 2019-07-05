# Numpy

> Numpy 用于数组和矢量计算
> CSV(Comma-Separated Value) Like a excel



## 操作单个数组的函数
+ array.ndim 数组维数
+ array.size 数组个数
+ array.itemsiz 数组每个元素的字节大小
+ abs、fabs、sqrt、square、exp、log、log10、log2、log1p
+ sign(正 1 负 0)、ceil、floor、rint(四舍五入)、modf(将数组小数和整数以两独立数组返回)
+ isnan(返回一个表示哪些值是 `NaN` 的布尔型数组)
+ isfinite、isinf（返回哪些元素有穷，哪些无穷的布尔型数组）
+ cos、cosh、sin、sinh、tan、tanh、arcos、arccosh、arcsin、arcsin、arctan



## 操作多个数组的方法
+ add、subtract、multipy、divide、floor_divide
+ power、maximum、fmax(忽略 NaN)
+ minmun、fmin(忽略 NaN)
+ mod、copysign(将第二个数组中的值得负号复制到第一个数组中的值)
+ greate、greate_equal、less、less_equal、equl、not_equal (产生布尔型数组)
+ logical_and、logical_or、logical_xor (&|^)
+ argmin, argmax (最大小值的索引)
+ cumsum cumprod (所有元素的累积和，累积积)



## savetxt 生成数据集
`np.savetxt(frame,array,fmt='%.18e",delimiter=None)`
+ frame 文件、字符串、或产生器的名字，可以是.gz, .bz2的压缩文件
+ arrray 存入文件的NP的数组
+ fmt(format) 写入文件的格式，如%d,%.2f,%.18e(默认，科学计数法保留18位)
+ delemiter 分割字符串，默认是任何空格



## loadtxt 读取数据集
`np.loadtxt(frame,dtype=np.float,delimiter=None,inpack=False)`
+ frame 指定读入的文件来源
+ dtype 数据类型，默认为 np.float
+ delimiter 分割字符串
+ unpack 默认为 False 读入文件写入一个数组，如果为 True，读入属性将分别写入不同变量

> CSV文件只能有效存储和读取一维和二维数组，因为更高的维度无法更直观的文本下显现出来



## tofile 写入文件
对于 NP 中的 ndarray 数组，我们可以使用 tofile 方法
`a.tofile(frame,sep='',format='%d')`
+ frame 文件，字符串
+ sep 数据分割字符串，如果不写，将使用二进制文件存储
+ format 写入数据的格式



## fromfile 读入文件
`np.fromfile(frame,dtype=float,count=-1,sep='')`
+ frame 文件
+ dtype 读取元素使用的数据类型，默认为 float
+ count 读文件的个数，默认 -1，读取全部
+ sep 数据分割字符串，如果是空串，写入文件为二进制

> 想要重新恢复数据的维度信息，我们需要重新使用 reshape 来恢复维度信息



## save | load 函数
> 保存 | 读取高维度数据

`np.save(frame, array) | np.savez(fname, array)(压缩)`
+ frame 文件名，以 .npy 为扩展名，压缩扩展名为 .npz
+ array 数组变量
`np.load(fname)`



## genfromtxt 读取 txt 文件
`numpy.genfromtxt()` 用于读取 txt 文件
+ 需要读取的 txt 文件位置，此处文件与程序位于同一目录下
+ 分割的标记
+ 转换类型，如果文件中既有文本类型也有数字类型，就先转成文本类型



## 类型转换
+ arr.astype(str)
+ arr.astype(float)



## 各种变换
+ arr.T 行列变换
+ arr.resize(1, 4) 变换结构 1row 4 column
+ 对应位置一次相乘 arr1 * arr2
+ 横向相加 np.hstack(a,b)
+ 纵向相加 np.vstack(a,b)
+ 横向分割 `print( np.hsplit(a,3))`
+ 纵向风格 `print(np.vsplit(a,3))`
+ numpy.transpose(arr, axes) equal to ndarray.T 逆置
+ rollaixs(arr, axis, start) 向后滚动指定轴，宽度方向 axis -> 默认从深度方向 start 0
+ swapaxes(arr, axis1, axis2)  互换数组两个轴，默认从深度方向 axis2 -> 宽度方向 axis1



## 拷贝
通过 b = a 复制 a 的值，b 与 a 指向同一地址，改变 b 同时也改变 a
`b.shape = (3,4)`
通过 a.view() 仅复制值, 当对 c 值进行改变会改变 a 的对应的值，而改变 c 的 shape 不改变 a 的 shape
a.copy() 进行的完整的拷贝，产生一份完全相同的独立的复制



## 数组的读取和存储 numpy.
+ save('xxx', arr)  对数组数据进行保存, 默认格式为.npy
+ load('xxx.npy') 读取已有的数组数据
+ loadtxt('xxx.txt', delimiter = ',') 从txt文件加载数据到一个数组
+ savetxt() 把数组保存在txt文件中



## 随机数生成
`numpy.random.random(10)` 随机数生成(0, 1) 10个。
其它形式的随机数生成方法：
+ seed 确定随机数生成器的种子
+ permutation 返回一个序列的随机排列或一个随机排列的范围
+ shuffle 对一个序列就地随机排列
+ rand 产生均匀分布的样本值
+ randn 产生正态分布(均值为0, 标准差为1)的样本值， 类似于matlab借口
+ binomial 产生二项分布的样本值
+ beta 产生Beta分布的样本值
+ chisquare 产生卡方分布的样本值
+ gamma 产生Gamma分布的样本值
+ uniform 产生在[0, 1）中均匀分布的样本值



## 矩阵
> 矩阵总是二维的，而 ndarray 是一个 n 维数组，两对象可以互换

+ NumPy 包包含一个 Matrix 库 numpy.matlib，此模块的函数返回矩阵
+ numpy.matlib.empty(shape, dtype, order)
+ numpy.matlib.zeros()
+ numpy.matlib.ones()
+ numpy.matlib.eye(n, M, k, dtype) n 返回矩阵的行数，M 返回矩阵的列数,，默认为 n，k 对角线的索引
+ np.matlib.eye(n = 3, M = 4, k = 0, dtype = float)
+ numpy.matlib.identity() 函数返回给定大小的单位矩阵，单位矩阵是主对角线元素都为 1 的方阵
+ np.matlib.rand(3,3) 函数返回给定大小的填充随机值的矩阵
+ np.asarray(i) matrix -> array
+ np.asmatrix (j) array -> matrix



## 线性代数常用方法
> NumPy 包包含 numpy.linalg 模块

+ dot 两个数组的点积，对于二维向量，其等效于矩阵乘法，对于一维数组，它是向量的内积
+ vdot 两个向量的点积，两个向量的点积
+ inner 两个数组的内积，向量内积，高的维度，它返回最后一个轴上的和的乘积
+ matmul 两个数组的矩阵积
+ determinant 数组的行列式
+ solve 求解线性矩阵方程
+ inv 寻找矩阵的乘法逆矩阵(方阵的逆)
+ numpy.linalg.det 函数计算输入矩阵的行列式
+ numpy.linalg.solve 函数给出了矩阵形式的线性方程的解
+ diag()  以一维数组的形式返回方阵的对角线(或非)元素, 或将一维数组转换放方阵
+ trace() 计算对角线元素的和
+ dot()   计算矩阵行列式
+ eig()   计算方阵的本征值和本征向量
+ inv()   计算方阵的逆
+ pinv()  计算矩阵的Moore-Penrose伪逆
+ qr()    计算QR分解
+ svd()   计算奇异值分解(SVD)
+ solve() 解线性方程组Ax = b, 其中A为一方阵
+ lstsq() 计算Ax = b的最小二乘解



## 广播知识
如果满足以下规则，可以进行广播：
1. ndim 较小的数组会在前面追加一个长度为 1 的维度。
2. 输出数组的每个维度的大小是输入数组该维度大小的最大值。
3. 如果输入在每个维度中的大小与输出大小匹配，或其值正好为 1，则在计算中可它。
4. 如果输入的某个维度大小为 1，则该维度中的第一个数据元素将用于该维度的所有计算。
5. 如果上述规则产生有效结果，并且满足以下条件之一，那么数组被称为可广播的。

> 数组拥有相同形状。数组拥有相同的维数，每个维度拥有相同长度，或者长度为 1，
> 数组拥有极少的维度，可以在其前面追加长度为 1 的维度，使上述条件成立



## 多维数组操作练习一
```python
import numpy

# 构造一个简单的数组
data = numpy.array([2, 5, 6, 8, 3])
print(data.shape) # 查看数组维度,一维数组,五个元素
print(data.dtype) # 查看数据格式, 32 位 int
print(data * 2) # 运算

# 构造一个二维数组
data = numpy.array([[2, 5, 6, 8, 3], numpy.arange(5)])

arr = numpy.arange(10)
print(arr[5]) # 索引
print(arr[5:8]) # slice index
arr[5] = 120 # 利用索引对数据进行更改

# 布尔操作
arr = numpy.arange(5)
name = numpy.array(['a', 'b', 'b', 'c', 'a'])
print(name == 'a') # 把判断的结果全部输出
print(arr[name == 'a']) # 利用数组 name 设置条件后的布尔值对 arr 进行操作, 把位置打印出来

### 多条件操作
name = numpy.array(['a', 'b', 'b', 'c', 'a'])
result = (name == "a") | (name == 'c')
print(result)
print(name[result])

### 生成多维矩阵
a, b = numpy.meshgrid(numpy.arange(1, 5), numpy.arange(2, 4))
print('a:\n', a) # 按照数据最少的数组形成数组
print('b:\n', b)

# numpy.where 三元表达式, x if condition else y 的矢量化版本

arr1 = numpy.arange(5)
arr2 = numpy.arange(20,25)
condition = numpy.array([1, 0, 1, 0, 0]) # bool
result = numpy.where(condition, arr1, arr2)
print(arr1)
print(arr2)
print(result)

### 数学统计方法
arr = numpy.random.randint(1, 20, 10) 
print(arr)
print(numpy.mean(arr))
print(numpy.sum(arr))
print(numpy.std(arr))

### 布尔型数组的相关统计方法
arr = numpy.arange(-20, 10)
result = (arr > 5).sum()
print(arr)
print(result)
```


## 多维数组操作练习二
```python
import numpy as np

# np 数组定义
lst = [[1, 3, 5], [2, 4, 6]]
np_lst = np.array(lst, dtype = np.float)
print(np_lst.shape) # 行列 (2, 3)
print(np_lst.ndim) # 维度 2
print(np_lst.dtype) # 数据类型 float64
print(np_lst.itemsize) # 每个元素的字节大小 8
print(np_lst.size) # 元素个数 6

# 初始化数组
print(np.zeros([2, 4])) # 初始化一个2行4列的数组 2 * 4 个 0
print(np.ones([2, 4])) # 2 * 4 个 1

# 随机序列
print(np.random.rand(2, 4)) # (0, 1)区间的 2 行 4 列的随机序列(不加参数只返回一个)

# 多个随机整数
print(np.random.randint(22, 55, 3)) # 前两参数知道范围, 第三参数指定生成个数
print(np.random.randn(2, 4)) # 生产标准正太随机数 2 行 4 列
print(np.random.choice([10, 20, 40, 33])) # 指定可迭代数组,随机生成里边的数
print(np.random.beta(1, 10, 4)) # 生成 4 个 beta 分布

# 多维数组运算
print(np.arange(1, 11, 2)) # [1 3 5 7 9]

# reshape函数对数组结构重定义
print(np.arange(1, 11).reshape(2, 5)) # 5 可缺省为 -1, (带三参数)

# 常用的运算操作
lst = np.arange(1, 11).reshape(2, 5) # 此为2行4列
print(np.exp(lst)) # 自然指数操作

# 试一下三维数组
lst = np.array([
    [[1, 2, 3, 4], [4, 5, 6, 7]],
    [[7, 8, 9, 10], [10, 11, 12, 13]],
    [[14, 15, 16, 17], [18, 19, 20, 21]]
])
print(lst.sum()) # 252

# 可通过 sum 方法增加参数 axis 来设置求和的深度(维度)，max 函数也可以
print(lst.sum(axis = 0))
# [[22 25 28 31]    22 = 1 + 7 + 14; 25 = 2 + 8 + 15
# [32 35 38 41]]

print(lst.sum(axis = 1))
# [[5  7  9 11]    5 = 1+ 4; 7 = 2 + 5
# [17 19 21 23]
# [32 34 36 38]]

print(lst.sum(axis = 2))
# [[10 22] 10 = 1 + 2 + 3 + 4; 22 = 4 + 5 + 6 + 7
# [34 46]
# [62 78]]

list1 = np.array([10, 20, 30, 40])
list2 = np.array([4, 3, 2, 1])
print(list1 + list2) # 一维相加
print()
print(np.dot(list1.reshape([2, 2]), list2.reshape([2, 2]))) # 行列式(矩阵相乘)

# 可声明各种常见数据类型如
# bool、int8/16/32/64/128/、uint8/16/32/64/128
# float16/32/43、complex64/128、string <U21

lst = np.array([np.arange(1, 6, 2), np.arange(2, 7, 2)])
print()
print(lst)
print(np.array(lst, dtype = np.float))

# numpy.genfromtxt() 用于读取 txt 文件
world_alcohol = np.genfromtxt("world_alcohol.txt", delimiter=",",dtype=str)
print(type(world_alcohol))
print(world_alcohol)
print(help(np.genfromtxt))
```



## 将数据导入文件操作
```python
import numpy

# 生成数据集
a = numpy.arange(20).reshape(4, 5)
numpy.savetxt('demo1.csv', a, fmt = '%d', delimiter = ',')

# 读取数据集
print(numpy.loadtxt('demo1.csv', dtype = numpy.float, delimiter = ','))

# tofile方法
b = numpy.arange(100).reshape(5, 10, 2)
b.tofile('demo2.dat', sep = ',', format = '%d')

print(numpy.fromfile('demo2.dat', dtype = numpy.int, sep = ','))
print(numpy.fromfile('demo2.dat', dtype = numpy.int, sep = ',').reshape(5, 10, 2))

# save load
a1 = numpy.arange(100).reshape(5, 5, 4)
numpy.save('demo3.npy', a1)
print(numpy.load('demo3.npy'))
```

