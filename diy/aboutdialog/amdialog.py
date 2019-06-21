from PyQt5.QtWidgets import QDialog, QApplication

from diy.aboutdialog.aboutme import Ui_Dialog
from diy.settings import update_log, version_code, app_name


class AMDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(AMDialog, self).__init__(parent)
        self.setupUi(self)
        self.textBrowser.setText(update_log)
        self.version_code.setText(version_code)
        self.app_name.setText('软件名称：%s' % app_name)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ui = AMDialog()
    ui.show()
    sys.exit(app.exec_())
