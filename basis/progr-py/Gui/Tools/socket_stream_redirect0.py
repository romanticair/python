"""
用于将非图形用户界面程序的流和套接字连接起来的工具（非完整实现）。通过套接字，图
形界面可与非图形界面实现交互；更完整的实现请参考后续的模块
"""
import sys
from socket import *

port = 50008
host = 'localhost'


def redirectOut(port=port, host=host):
    """
    将呼叫方的标准输出流连接到一个套接字，供图形用户界面监听；监听方开启之后才
    开启呼叫方，否则连接失败，无法接受。
    """
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))              # 呼叫方以客户模式运行
    file = sock.makefile('w')               # 文件接口：文本，已缓存
    sys.stdout = file                       # 使打印的文件进入sock.send

def redirectIn(port=port, host=host):...                # 请看后面的套接字介绍
def redirectBothAsClient(port=port, host=host):...    # 请看后面的套接字介绍
def redirectBothAsServer(port=port, host=host):...    # 请看后面的套接字介绍