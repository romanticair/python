import sys
from PyQt5.QtWidgets import QApplication
from ui_slot import UserWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = UserWindow()
    exe.show()
    sys.exit(app.exec())