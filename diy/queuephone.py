from queue import Queue

from diy.settings import printlog


class MsgQueuePhone:
    def __init__(self, sourcedata: str, type: int):
        self.type = type
        single_data_list = sourcedata.split()
        self.air_pressure = float(single_data_list[0])
        self.force = float(single_data_list[1])
        self.displacement = float(single_data_list[2])

    def getdata(self):
        if self.type == 1:
            printlog('air_pressure,force')
            return self.air_pressure, self.force
        elif self.type == 2:
            printlog('displacement,force')
            return self.displacement, self.force
        elif self.type == 3:
            printlog('air_pressure,displacement')
            return self.air_pressure, self.displacement
        else:
            return 0, 0


class QueuePhone(Queue):
    def insert_sim(self, sim_type):
        self.type = sim_type
        self.block = False

    def send_message(self, msg):
        self.put(MsgQueuePhone(msg, self.type))

    def receive_message(self):
        msg = self.get()
        # print('receive:%s' % msg)

        if msg:
            # print(msg.getdata())
            return msg.getdata()
