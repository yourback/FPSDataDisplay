from PyQt5.QtWidgets import QDialog, QApplication

from diy.aboutdialog.aboutme import Ui_Dialog


class AMDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(AMDialog, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ui = AMDialog()
    ui.show()
    sys.exit(app.exec_())
