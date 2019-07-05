"""
通过 psutil 第三方模块获取系统信息

用Python来编写脚本简化日常的运维工作是Python的一个重要用途。
在Linux下，有许多系统命令可以让我们时刻监控系统运行的状态，如ps，
top，free等等。要获取这些系统信息，Python可以通过subprocess模块调
用并获取结果。但这样做显得很麻烦，尤其是要写很多解析代码。
"""
import psutil

# 1.获取CPU信息
print(psutil.cpu_count())  # CPU逻辑数量
print(psutil.cpu_count(logical=False))  # CPU物理核心
# result -> 2说明是双核超线程, 4则是4核非超线程

# 2.统计CPU的用户／系统／空闲时间
print(psutil.cpu_times())
# scputimes(user=96387.0, system=56166.78125, idle=404438.84375, interrupt=2352.21875, dpc=1321.6562509536743)

# 3.再实现类似top命令的CPU使用率，每秒刷新一次，累计10次
for x in range(10):
    print(psutil.cpu_percent(interval=1, percpu=True))

# 4.获取内存信息
# 获取物理内存和交换内存信息，分别使用
print(psutil.virtual_memory())
# svmem(total=8589934592, available=781422592, percent=81.4, used=3425738752, free=781422592)
print(psutil.swap_memory())
# sswap(total=1073741824, used=6019141632, free=2504531968, percent=70.6, sin=0, sout=0)

# 返回的是字节为单位的整数，可以看到，总内存大小是8589934592 = 8 GB，已用81.4%，
# 使用了66.6%。而交换区大小是1073741824 = 1 GB

# 5.获取磁盘信息
# 获取磁盘分区、磁盘使用率和磁盘IO信息
print(psutil.disk_partitions())
"""
[sdiskpart(device='C:\\', mountpoint='C:\\', fstype='NTFS',
opts='rw,fixed'), sdiskpart(device='D:\\', mountpoint='D:\\',
fstype='', opts='cdrom'), sdiskpart(device='E:\\', mountpoint='E:\\',
fstype='NTFS', opts='rw,fixed'), sdiskpart(device='F:\\', mountpoint='F:\\',
fstype='NTFS', opts='rw,fixed'), sdiskpart(device='L:\\', mountpoint='L:\\',
fstype='NTFS', opts='rw,fixed')]
"""
print(psutil.disk_usage('/'))  # 磁盘使用情况
# sdiskusage(total=41943035904, used=19852169216, free=22090866688, percent=47.3)
print(psutil.disk_io_counters())  # 磁盘IO
# sdiskio(read_count=2571296, write_count=1599285, read_bytes=91084611584,
# write_bytes=69997443072, read_time=114446, write_time=34695)

# 磁盘'/'的总容量是41943035904 = 400 GB
# 文件格式是HFS，opts中包含rw表示可读写，journaled表示支持日志。

# 6.获取网络信息
# 获取网络接口和网络连接信息
print(psutil.net_io_counters())  # 获取网络读写字节／包的个数
print(psutil.net_if_addrs())  # 获取网络接口信息
print(psutil.net_if_stats())  # 获取网络接口状态
print(psutil.net_connections())  # 获取当前网络连接信息

# 7.获取进程信息
print(psutil.pids)  # 所有进程ID
p = psutil.Process(3776)  # 获取指定进程ID=3776，其实就是当前Python交互环境
print(p.name)  # 进程名称
print(p.exe)  # 进程exe路径
print(p.cwd())  # 进程工作目录
print(p.cmdline())  # 进程启动的命令行
print(p.ppid())  # 父进程ID
print(p.parent())  # 父进程
print(p.children())  # 子进程列表
print(p.status())  # 进程状态
print(p.username())  # 进程用户名
print(p.create_time())  # 进程创建时间
print(p.terminate())  # 进程终端
print(p.cpu_times())  # 进程使用的CPU时间
print(p.memory_info())  # 进程使用的内存
print(p.open_files())  # 进程打开的文件
print(p.connections())  # 进程相关网络连接
print(p.num_threads())  # 所有线程信息
print(p.environ())  # 进程环境变量
p.terminate()  # 结束进程 -> 把自己结束了
