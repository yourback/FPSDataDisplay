# -*- coding: utf-8 -*-
"""
Various methods of drawing scrolling plots.
"""
import sys

import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow
import numpy as np


class GraphView(QMainWindow):

    def __init__(self, parent=None):
        win = pg.GraphicsWindow()
        win.setWindowTitle('pyqtgraph example: Scrolling Plots')
        self.p4 = win.addPlot()
        self.p4.setDownsampling(mode='peak')
        self.p4.setClipToView(True)
        self.curve4 = self.p4.plot()

        self.data3 = np.empty(100)
        self.ptr3 = 0

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)

    def update(self):
        self.data3[self.ptr3] = np.random.normal()
        self.ptr3 += 0.1
        print("self.ptr3:%s" % self.ptr3)
        print("self.data3.shape[0]:%s" % self.data3.shape[0])
        if self.ptr3 >= self.data3.shape[0]:
            tmp = self.data3
            data3 = np.empty(self.data3.shape[0] * 2)
            data3[:tmp.shape[0]] = tmp

        self.curve4.setData(self.data3[:self.ptr3])

    def start_update(self):
        self.timer.start(2.5)

    def pause_update(self):
        self.timer.stop()


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    # import sys
    #
    # if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    #     QtGui.QApplication.instance().exec_()
    app = QApplication(sys.argv)
    gv = GraphView()
    # gv.start_update()
    sys.exit(app.exec_())
