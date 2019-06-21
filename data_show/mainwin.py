from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow

from data_save.saveprogram import save_excel
from data_show.datashow import Ui_MainWindow

import pyqtgraph as pg
import serial.tools.list_ports

from diy.queuephone import QueuePhone
from diy.settings import port_time, printlog

from data_source.portworker import PortWorker


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        pg.setConfigOption('background', '#fff')  # 设置背景为灰色
        pg.setConfigOption('foreground', '#000')  # 设置前景（包括坐标轴，线条，文本等等）为黑色。

        pg.setConfigOptions(antialias=True)  # 使曲线看起来更光滑，而不是锯齿状

        self.setupUi(self)

        # combobox group action
        self.cbb_group.currentIndexChanged.connect(self.cbb_group_changed)
        # combobox group action
        self.cbb_port.currentIndexChanged.connect(self.cbb_port_changed)

        # init pyqtgraph
        self.initpg()

        # init btn status
        self.btn_status(False)

        # combobox port init
        self.cbb_port_init()

        # buy a new phone
        self.phone_queue = QueuePhone()

    def cbb_port_init(self):
        '''
        init of combobox (select  port)
        :return:
        '''
        self.cbb_group.setEnabled(False)

        # data
        # self.cbb_port.clear()
        self.port_list = list(serial.tools.list_ports.comports())
        if len(self.port_list) != 0:
            for port in self.port_list:
                # printlog(type(port))
                self.cbb_port.addItem(port.__str__())

    @pyqtSlot()
    def on_btn_port_clicked(self):
        if self.btn_port.text() == '打开串口':
            self.btn_port.setText('关闭串口')
            self.btn_pause.setText("暂停")
            self.btn_pause.setEnabled(True)
            self.cbb_group.setEnabled(False)
            self.cbb_port.setEnabled(False)

            # hire worker and give him the phone
            self.port_worker = PortWorker(paintdata=self.phone_queue, portnum=self.port)
            # let worker work
            self.start_save()

            self.timer.start(port_time * 10)
        else:
            self.btn_port.setText('打开串口')
            self.btn_pause.setEnabled(False)

            # fire the portworker
            self.port_worker.pause = True
            self.port_worker.working = False

            self.timer.stop()

            # rename the excel file
            # 'temple_data.xls'
            save_excel(self)

    def start_save(self):
        # let worker worker
        self.port_worker.working = True
        self.port_worker.pause = False
        self.port_worker.start()

    @pyqtSlot()
    def on_btn_pause_clicked(self):
        printlog('btn_pause click')
        if self.btn_pause.text() == '继续' or self.btn_pause.text() == '开始':
            self.timer.start(port_time * 10)
            self.port_worker.pause = False
            self.btn_pause.setText("暂停")
        else:
            self.timer.stop()
            self.port_worker.pause = True
            self.btn_pause.setText("继续")

    @pyqtSlot()
    def on_btn_refresh_port_clicked(self):
        printlog('on_btn_refresh_port_clicked')
        self.cbb_port_init()

    @pyqtSlot()
    def on_btn_clear_paint_clicked(self):
        printlog('on_btn_clear_paint_clicked')
        self.x_data.clear()
        self.y_data.clear()
        self.curve.setData(self.x_data, self.y_data)
        QApplication.processEvents()

    def cbb_group_changed(self, i):
        if i == 0:
            self.btn_status(False)
        else:
            # insert a sim card into phone
            self.phone_queue.insert_sim(i)
            self.btn_port.setEnabled(True)
        self.set_label(i)

    def cbb_port_changed(self, i):
        if i == 0:
            self.cbb_group.setEnabled(False)
        else:
            self.cbb_group.setEnabled(True)
            self.port = self.port_list[i - 1].device

    def initpg(self):
        '''
        init pg
        :return:
        '''
        self.p = self.widget.addPlot()
        self.p.setDownsampling(mode='peak')
        self.p.setClipToView(True)
        self.curve = self.p.plot(pen='#000')

        # data
        self.x_data = [0, ]
        self.y_data = [0, ]
        # update timer
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)

    def set_label(self, i):
        '''
        :param i:
        i == 0 没有选择
        i == 1 气压-力，力是纵坐标
        i == 2 位移-力，力是纵坐标
        i == 3 气压-位移，位移是纵坐标
        :return:
        '''
        if i == 0:
            self.p.setLabel('bottom', '', '')
            self.p.setLabel('left', '', '')
        elif i == 1:
            self.p.setLabel('bottom', '气压', '')
            self.p.setLabel('left', '力', '')
        elif i == 2:
            self.p.setLabel('bottom', '位移', '')
            self.p.setLabel('left', '力', '')
        elif i == 3:
            self.p.setLabel('bottom', '气压', '')
            self.p.setLabel('left', '位移', '')

    def update(self):
        # get data from queue and show it
        # get data
        printlog('主线程开始收数据')

        current_data = self.phone_queue.receive_message()

        if current_data:
            data_1, data_2 = current_data

            printlog('主线程收到数据：%s,%s' % (data_1, data_2))
            self.x_data.append(data_1)
            self.y_data.append(data_2)

            # printlog('x_data:%s' % self.x_data)
            # printlog('y_data:%s' % self.y_data)

            self.curve.setData(self.x_data, self.y_data)

    def btn_status(self, able):
        self.btn_pause.setEnabled(able)
        self.btn_port.setEnabled(able)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
