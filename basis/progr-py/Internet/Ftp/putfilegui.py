"""
#####################################################################################
启动带有可复用的表单GUI类的FTP putfile函数，请参考getfilegui里的说明：大部分缺陷
仍然适用，get和put表单归纳为一个类，这样修改时只需在一处进行。
#####################################################################################
"""
from tkinter import mainloop
import putfile
import getfilegui


class FtpPutfileForm(getfilegui.FtpForm):
    title = 'FtpPutfileGui'
    mode = 'Upload'

    def do_transfer(self, filename, servername, remotedir, userinfo):
        putfile.putfile(filename, servername, remotedir, userinfo, verbose=False)

if __name__ == '__main__':
    FtpPutfileForm()
    mainloop()
