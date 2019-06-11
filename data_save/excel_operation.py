import xlwt


class ExcelOperation:
    file_name = 'temple_data.xls'

    def __enter__(self):
        return self

    def __init__(self):
        self.row = 0
        # self.file_name = datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.xls'
        self.book = xlwt.Workbook()  # create a new excel file
        self.sheet = self.book.add_sheet('data')  # add a sheet into excel
        self.sheet.write(0, 0, 'air pressure')  # insert title pressure
        self.sheet.write(0, 2, 'force')  # insert title force
        self.sheet.write(0, 4, 'displacement')  # insert title displayment

    def write_data(self, data):
        # print('write_data:%s' % data)
        single_data_list = data.split()
        self.sheet.write(self.row, 1, single_data_list[0])
        self.sheet.write(self.row, 3, single_data_list[1])
        self.sheet.write(self.row, 5, single_data_list[2])
        self.row += 1

    def close(self):
        self.book.save(self.file_name)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == '__main__':
    with ExcelOperation() as eo:
        # eo.write_data('111 222 333')
        pass
