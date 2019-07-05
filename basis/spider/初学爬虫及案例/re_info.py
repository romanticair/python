
# 1.原子:

"""
\w 匹配任意一个字母,数字或下划线
\W 除\w之外的
\d 匹配任意一个十进制数
\D 除\d之外的
\s 匹配任意一个空白字符
\S 除\s之外的
"""

# 原子表由[]表示, 匹配时取表中任意一原子进行匹配, abc三个原子
# [xyz]py  [^] 相反

# 2.元字符:
"""
. 匹配除换行符以外任意字符
^ 匹配字符串开始位置      必须以...开头
$ 匹配字符串结束位置      必须以...结尾
* 匹配任意次前面的原子
? 匹配0次或一次前面的原子
+ 匹配1次或多次前面的原子
{n} 前面原子恰好出现n次
{n,} 前面原子至少出现n次
{n,m} 前面原子至少出现n此, 至多出现m次
| 模式选择符    满足其一条件即可
() 模式单元符
"""

# pattern1 = "(cd)(1,)"   cd被看成一个整体
# pattern1 = "cd(1,)"
# string = "abcdcdcdcdkjdgdjlg-oy"
# result1 = re.search(pattern1, string)
# result2 = re.search(pattern2, string)
# 1: match = 'cdcdcdcd', 2: match = 'cd'

# 3.模式修正:

"""
I 忽略大小写
M 多行匹配
L 做本地化识别匹配
U 根据Unicode字符及解析字符
S 使.匹配包括换行符  (相当于匹配任意字符)

"""

# pattern = "python"
# s = "abcdkdPython_pupi"
# result = re.search(pattern, s, re.I)
# match = "Python"

# 贪婪模式与懒惰模式:

# pattern1 = "p.*y" 贪婪模式   (尽多的匹配, 找不到为止)
# pattern2 = "p.*?y" 懒惰模式  (就近匹配原则, 找到则止)
# string = "abcdfphp345pythony_py"
# result1 = re.search(pattern1, string)
# result2 = re.search(pattern2, string)
# match1: match = 'php345pythony_py'
# match2: match = 'php345py'


# re.match(pattern, string, flag) 起始位置匹配一个模式
# .span() 可以过滤掉一些信息, 只留结果的位置
# re.search(pattern, string) 全文检索匹配

# 源字符串有多个结果符合模式, 但上面函数只匹配一结果

# 可以使用以下思路匹配除全部结果
# 1.用re.compile() 对正则表达式进行预编译
# 2.用findall()根据正则表达式从源字符串中将匹配的结果全部找出
"""
import re
string = "hellomypythonhispythonourpythonend"
pattern = re.complie(".python.") 预编译
result = pattern.findall(string) 找出符合模式的所有结果
print(result)
['ypythonh', 'spythono', 'rpythone']

"""

# 替换re.sud(pattern, rep, string, max) max: 替换次数, 默认全部替换


# Cookiejar:
# HTTP协议: 无状态协议即无法维持回话之间的状态
# 登录都涉及到Cookie
# 会话信息控制常用的方式有两种
# 1.Cookie保存会话信息
# 2.Session保存会话信息 -> 将会话信息保存在服务器端, But
# 服务器端会给客户发送SessionID等信息, 这些信息一般存在客户端Cookie中,
# 所以用户大部分信息存在Cookie中

# 要获得真实的登录地址, 分析方式主要有两种:
# 1.F12调出调试界面进行分析,
# 2.用工具软件进行分析, 常用工具: Fiddler.

'http://bbs.chinaunix.net/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=Lo9UZ'


