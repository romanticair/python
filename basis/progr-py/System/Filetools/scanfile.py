def scanner(name, function):
    file = open(name, 'r')       # 创建文件对象
    while True:
        line = file.readline()
        if not line:            # 直到文件末尾
            break
        function(line)           # 调用函数对象
    file.close()