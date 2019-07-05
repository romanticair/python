"""
用 asyncio 提供的 @asyncio.coroutine 可以把一个 generator 标记为 coroutine 类型
然后在 coroutine 内部用 yield from 调用另一个coroutine实现异步操作

async 和 await 是针对 coroutine 的新语法，要使用新的语法，只需两步简单的替换
1. 把@asyncio.coroutine替换为async
2. 把yield from替换为await
"""
import asyncio


@asyncio.coroutine
def hello():
    print("Hello world!")
    r = yield from asyncio.sleep(1)
    print("Hello again!")

async def hello():
    print("Hello world!")
    r = await asyncio.sleep(1)
    print("Hello again!")
