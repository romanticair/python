"""
asyncio的编程模型就是一个消息循环,从asyncio模块中直接获取一个EventLoop的引用，
然后把需要执行的协程扔到 EventLoop 中执行，就实现了异步 IO

异步操作需要在coroutine中通过yield from完成
多个coroutine可以封装成一组Task然后并发执行
"""
import asyncio


def hello_world_by_asyncio():
    """
    用asyncio实现Hello world
    """
    @asyncio.coroutine  # 把一个generator标记为coroutine类型
    def hello(index):
        print("Hello world! %d" % index)
        # 异步调用asyncio.sleep(1)
        # yield from语法可以让我们方便地调用另一个generator, 拿到返回值
        r = yield from asyncio.sleep(1)
        print("Hello again! %d" % index)

    # 获取EventLoop
    loop = asyncio.get_event_loop()
    tasks = [hello(1), hello(2)]
    # 执行coroutine
    loop.run_until_complete(asyncio.wait(tasks))  # 把这个coroutine扔到EventLoop中执行
    loop.close()


# 执行
hello_world_by_asyncio()


def get_web():
    """
    用 asyncio 的异步网络连接来获取sina、sohu和163的网站首页
    """
    @asyncio.coroutine
    def wget(host):
        print('wget %s...' % host)
        connect = asyncio.open_connection(host, 80)
        reader, writer = yield from connect
        header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
        writer.write(header.encode('utf-8'))
        yield from writer.drain()
        while True:
            print('!!!!!!!!!!!Stop here!!!!!!!!!!!!!')
            line = yield from reader.readline()
            if line == b'\r\n':
                break
            print('%s header > %s' % (host, line.decode('utf-8').rstrip()))

        # Ignore the body, close the socket
        writer.close()

    loop = asyncio.get_event_loop()
    tasks = [wget(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

get_web()
