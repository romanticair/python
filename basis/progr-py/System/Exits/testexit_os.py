def outahere():
    import os
    print('Bye os world')
    # try/except 和 try/finally截获对此均不起作用
    os._exit(99)
    print('nerver reached')

if __name__ == '__main__':
    outahere()