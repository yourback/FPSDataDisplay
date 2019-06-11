import re
from queue import Queue

from PyQt5.QtCore import QThread

from data_save.excel_operation import ExcelOperation
from data_source.Interface import PortManager
from diy.settings import printlog


class PortWorker(QThread):
    working = True
    pause = False

    def __init__(self, paintdata, portnum):
        super(PortWorker, self).__init__()
        # portworker get a phone
        self.paint_queue = paintdata
        self.port_num = portnum

    def run(self):
        # open port
        with PortManager(self.port_num) as pm:
            source_data = pm.get_data_from_interface()
            i = 0
            # open excel
            with ExcelOperation() as eo:
                for d in source_data:
                    # print('串口传来的原始数据：%s\n其长度为：%s' % (d, len(d)))
                    if len(d) >= 53:
                        # try:
                        #     print('读一行数据：%s' % d.decode('utf-8'))
                        #
                        # except Exception as ex:
                        #     print("读取出错：%s" % ex)

                        if self.working:
                            s = d.decode('utf-8')
                            search = re.match(r'air pressure:(.*)\s*force:(.*)\s*displacement:(.*)\s*', s, re.M | re.I)
                            if search:
                                save_data = '%s %s %s' % (search.group(1), search.group(2), search.group(3))
                                # print(save_data)
                                printlog('get data from port:%s' % save_data)
                                # save data into excel
                                eo.write_data(save_data)
                                # i++
                                i += 1

                                # if not pause return data or ''
                                if not self.pause and i >= 10:
                                    i = 0
                                    self.paint_queue.send_message(save_data)
                        else:
                            printlog('break')
                            break
                # printlog('end _ExcelOperation')
            # printlog('end _PortManager')

        # printlog('thread end')


if __name__ == '__main__':
    q = Queue()

    pw = PortWorker(paintdata=q, portnum='com4')
    pw.start()

    i = 0

    while True:
        if not q.empty():
            print('%s主线程得到：%s' % (i, q.get()))
            i += 1
            if i == 10:
                pw.working = False
