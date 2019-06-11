import serial

from diy.settings import port_time, printlog


class PortManager:

    def __init__(self, port_num):
        super(PortManager, self).__init__()
        self.port_num = port_num
        self.ser = serial.Serial(self.port_num, 115200, timeout=port_time)  # windows系统使用com8口连接串行口
        # self.port_num = port_num

    def close_port(self):
        if self.ser is not None:
            self.ser.close()

    # def interface_swicth(self, b):
    #     try:
    #         if self.ser is not None:
    #             self.ser = serial.Serial(self.port_num, 115200, timeout=0.5)  # winsows系统使用com8口连接串行口
    #         if b:
    #             print('打开端口')
    #             if not self.ser.is_open:
    #                 self.ser.open()
    #         else:
    #             print('关闭端口')
    #             if self.ser.is_open:
    #                 self.ser.close()
    #         return True
    #     except Exception as e:
    #         print('错误')
    #         print(e)
    #         return False

    def get_data_from_interface(self):
        if not self.ser.is_open:
            printlog('端口开启')
            self.ser.open()  # enable port
        else:
            printlog('端口已经开启')

        while True:
            line_str = self.ser.readline()
            # print(line_str)
            yield line_str

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_port()


if __name__ == '__main__':
    import re

    with PortManager('com4') as pm:
        source_data = pm.get_data_from_interface()
        for d in source_data:
            s = d.decode('utf-8')
            search = re.match(r'air pressure:(.*)\s*force:(.*)\s*displacement:(.*)\s*', s, re.M | re.I)
            if search:
                print(search.group(1))
                print(search.group(2).strip())
                print(search.group(3).strip())
