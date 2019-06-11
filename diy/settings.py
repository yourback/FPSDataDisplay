# 2019年6月6日 需求
# 图像白底黑字    搞定
# excel表自主命名    关闭端口的时候
# 是否可以折线图保存 搞定


port_time = 0.25
is_log = False


def isprint(func):
    def isprint_in(str):
        if is_log:
            func(str)

    return isprint_in


@isprint
def printlog(str):
    print(str)


if __name__ == '__main__':
    printlog('good')
