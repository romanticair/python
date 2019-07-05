from PyQt5.QtWidgets import QMainWindow

from ui import Ui_MainWindow
from verify_dialog_slot import VerifyDialog


class UserWindow(QMainWindow, Ui_MainWindow):
    """
    Main Window.

    Separate system window's interface and logic.
    """

    def __init__(self):
        super(UserWindow, self).__init__()
        self.setupUi(self)
        self.hide_main_show_dialog()

    def hide_main_show_dialog(self):
        """
        Hide the main window and show the login dialog.
        """
        self.hide()
        self.dialog = VerifyDialog()
        self.dialog.ok_signal.connect(self.ok_slot)
        self.dialog.exec()

    def ok_slot(self, ok):
        """
        A slot was connected by login dialog's signal.
        Receive the result correct or not of user's input by parameter ok.

        :param ok:
        """
        if ok:
            self.dialog.close()
            self.show()




