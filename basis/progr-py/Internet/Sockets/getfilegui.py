"""
使用一个可复用的GUI表单类启动getfile客户端；如果有输入(getfile存储在命令行中)，
os.chdir就会指向本地目录，即将做的：使用线程，显示下载状态和getfile输出；
"""
import os
from tkinter import Tk, mainloop
from tkinter.messagebox import showinfo
import getfile
from form import Form


class GetFileForm(Form):
    def __init__(self, oneshot=False):
        root = Tk()
        root.title('getfilegui')
        labels = ['Server Name', 'Port Number', 'File Name', 'Local Dir?']
        Form.__init__(self, labels)
        self.oneshot = oneshot

    def onSubmit(self):
        Form.onSubmit(self)
        localdir = self.content['Local Dir?'].get()
        portnumber = self.content['Port Number'].get()
        servername = self.content['Server Name'].get()
        filename = self.content['File Name'].get()
        if localdir:
            os.chdir(localdir)
        portnumber = int(portnumber)
        getfile.client(servername, portnumber, filename)
        showinfo('getfilegui', 'Download complete')
        if self.oneshot:
            Tk().quit()

if __name__ == '__main__':
    GetFileForm()
    mainloop()
