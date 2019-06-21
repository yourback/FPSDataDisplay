# 2019年6月6日 需求
# 图像白底黑字    搞定
# excel表自主命名    关闭端口的时候
# 是否可以折线图保存 搞定


port_time = 0.25
is_log = True

# version code
version_code = '当前版本号：V0.3'

# app name
app_name = '外骨骼测试平台'

# update log
update_log = '''日期：2019年6月21日
版本：V0.3
1.添加端口检测，每5s进行一次扫描，如果端口数量发生变化则更新界面
2.修复若干BUG



日期：2019年6月11日 
版本：V0.2
1.图像白底黑字
2.最后生成的excel表支持自主命名
3.折线图可以作为图片保存



日期：2019年6月6日 
版本：V0.1
1.通过按钮设置串口的开闭，控制数据的采集
2.串口采集的到三组数据力，气压和位移，两两实时绘图。例如，通过串口采集到的力和气压的值，实时绘制力-气压曲线，直到本次测试结束
3.串口采集数据的速度比较快，平均2.5ms采集一个数，绘制曲线过程中如果有卡顿，可以选择没间隔几个点绘图
4.绘图的同时，将采集的数据保存在excel中（excel中的数据是完整数据）
5.采集过程中，可以随时暂停查看图形，查看完毕以后继续显示图形'''


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
