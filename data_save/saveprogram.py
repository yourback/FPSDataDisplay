from PyQt5.QtWidgets import QFileDialog
import os


def save_excel(self):
    f_name, _ = QFileDialog.getSaveFileName(self, '保存程序', '.', '*.xls')
    if f_name:
        os.rename('temple_data.xls', f_name)
