import sys
from PyQt5.QtWidgets import QApplication
from system_ui_slot import MyWin


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyWin()
    win.show()
    sys.exit(app.exec_())