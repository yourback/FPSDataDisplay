from PyQt5.QtWidgets import QComboBox


class ComboxAdjust(QComboBox):

    def dropEvent(self, *args, **kwargs):
        print('hhh')

    def adjustComboBoxDropDownListWidth(self):
        print('下拉了')
