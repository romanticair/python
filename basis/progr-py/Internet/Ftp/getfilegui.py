"""
#############################################################################################
启动带有可复用的表单GUI类的FTP getfile函数；使用os.chdir进入目标本地目录（目前getfile假定
文件名不带有本地目录路径前缀）；在线程中运行getfile.getfile，以便允许多个同时运行并避免在
下载过程中阻塞GUI；这一点和基于套接字的getfilegui不同，但它复用了GUI表单生成器工具；当前
版本同时支持用户匿名FTP；

缺陷：密码文本域在这里不能以星号显示，错误打印到控制台，而不是在GUI里显示（在Windows下线程
一般不能更新GUI），这一点并非100%线程安全的（这里os.chdir和getfile打开本地输出文件之间有一点
点延迟），另外我们还可以在选择本地目录时显示“另存为”弹出对话框，以及在选择待下载的文件时显
示远程目录；可作出相应改进。
#############################################################################################
"""
import os
import sys
import _thread
import getfile                            # 这里导入基于FTP的getfile，而非基于套接字的
from tkinter import Tk, mainloop
from tkinter.messagebox import showinfo
from Internet.Sockets.form import Form   # 复用套接字目录下的表单工具


class FtpForm(Form):
    def __init__(self):
        root = Tk()
        root.title(self.title)
        labels = ['Server Name', 'Remote Dir', 'File Name', 'Local Dir', 'User Name?', 'Password?']
        Form.__init__(self, labels, root)
        self.mutex = _thread.allocate_lock()
        self.threads = 0

    def transfer(self, filename, servername, remotedir, userinfo):
        try:
            self.do_transfer(filename, servername, remotedir, userinfo)
            print('%s of "%s" successful' % (self.mode, filename))
        except:
            print('%s of "%s" failed:' % (self.mode, filename), end='')
            print(sys.exc_info()[0], sys.exc_info()[1])
        self.mutex.acquire()
        self.threads -= 1
        self.mutex.release()

    def onSubmit(self):
        Form.onSubmit(self)
        localdir = self.content['Local Dir'].get()
        remotedir = self.content['Remote Dir'].get()
        servername = self.content['Server Name'].get()
        filename = self.content['File Name'].get()
        username = self.content['User Name?'].get()
        password = self.content['Password?'].get()
        userinfo = ()
        if username and password:
            userinfo = (username, password)
        if localdir:
            os.chdir(localdir)
        self.mutex.acquire()
        self.threads += 1
        self.mutex.release()
        ftpargs = (filename, servername, remotedir, userinfo)
        _thread.start_new_thread(self.transfer, ftpargs)
        showinfo(self.title, '%s of "%s" started' % (self.mode, filename))

    def onCancel(self):
        if self.threads == 0:
            Tk().quit()
        else:
            showinfo(self.title, 'Cannot exit: %d threads running' % self.threads)


class FtpGetfileForm(FtpForm):
    title = 'FtpGetFileGui'
    mode = 'Download'

    def do_transfer(self, filename, servername, remotedir, userinfo):
        getfile.getfile(filename, servername, remotedir, userinfo, verbose=False, refetch=True)

if __name__ == '__main__':
    FtpGetfileForm()
    mainloop()
