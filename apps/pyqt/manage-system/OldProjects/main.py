import sys
from PyQt5.QtWidgets import QApplication

from init import Init
from user import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    initWindow = Init()
    mainWindow = MainWindow()

    initWindow.loginButton.clicked.connect(mainWindow.handle_visible)
    initWindow.loginButton.clicked.connect(initWindow.hide)
    initWindow.close_signal.connect(initWindow.close)
    initWindow.show()
    sys.exit(app.exec_())