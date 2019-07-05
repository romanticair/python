1.程序为一系统用户登录界面
2.在 bin 目录下有已打包成 ui.exe 的可执行文件，和一个记录用户数据的 users.json 文件
3.users.json 中的数据已用 md5 加密过，在界面登录时可用账号: 123， 密码: abc 登录测试，
  该数据段已加密存进 users.json 文件。
4.所有源代码都在 login_interface 模块，运行程序入口文件为 main.py
5.register.py 为向 users.json 文件存入加密数据的程序文件
6.ui_lost.py 为系统主界面的业务逻辑程序
7.verify_dialog_slot.py 为系统登录对话框的业务逻辑程序
8.apprcc_rc.py 为系统内部的资源文件

说明：
  tests 和 docs 目录下的程序与根目录下的 setup.py 未完善