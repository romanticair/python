import urllib.request
import urllib.error

if __name__ == '__main__':
    """
    异常处理神奇 -- - - URLError
    第一个类: URLError
    第二个类: HTTPError
    """
    # 第一个实例
    try:
        urllib.request.urlopen("http://blog.csdn.net")
    except urllib.error.URLError as e:
        print(e.code)
        print(e.reason)

    """
    1.连接不上服务器
    2.远程URL不存在
    3.无网络
    4.触发了HTTPError
    """
    try:
        urllib.request.urlopen("http://blog.csdn.net")
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.reason)

    # 改进
    try:
        urllib.request.urlopen("http://blog.csdn.net")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):   # 目标地址存在, 引发异常时才有code
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)