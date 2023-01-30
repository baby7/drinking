# coding:utf-8
import os
import sys
import base64
import time
import datetime
import config
import record_list
from winotify import Notification
import icon.icon as icon
import darkdetect
from PyQt5.QtCore import Qt
from qframelesswindow import AcrylicWindow
from PyQt5.QtGui import QCursor
from main_form import Ui_Form
from setting import SettingWindow
from record import RecordWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QApplication, QMenu, QAction, QSystemTrayIcon)
import util.thread_util
import time_thread

"""
pyinstaller -F -w -i D:/project/python/drinking/icon/favicon.ico -n Windows喝水记录工具v2.0 main.py
"""
class Window(AcrylicWindow, Ui_Form):

    m_flag = None
    m_Position = None

    schedule = 0                    # 当前喝水杯数

    theme = "Acrylic"               # 主题类型 Acrylic为亚克力 Aero为玻璃
    theme_color = "auto"            # 主题颜色，主题为亚克力时可以选择自动(auto)、深色(dark)、浅色(light)

    color_white = "#303030"
    color_dark = "#FFFFFF"
    text_color = "#FFFFFF"
    line_color = 255

    sys_icon = None
    tray_icon = None

    pen = None
    background_arc_pen = None

    setting_win = None
    record_win = None

    remind_interval = 30
    drinking_count = 6
    view_message = "positive"
    view_top = "normal"

    dialog_fault = None

    time_thread = None
    time_add_count = 0

    active_time_list = None

    def __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)
        # 设置图标
        with open('tmp.ico', 'wb') as tmp:
            tmp.write(base64.b64decode(icon.Icon().ig))
        self.sys_icon = QIcon('tmp.ico')
        self.setWindowIcon(self.sys_icon)
        os.remove("tmp.ico")

        # 窗口属性
        self.setWindowFlags(Qt.SplashScreen)                    # 飞溅屏幕，窗口无边框化，无任务栏窗口

        # 设置标题栏
        self.setWindowTitle("Windows喝水记录工具")
        self.titleBar.raise_()
        self.titleBar.minBtn.close()
        self.titleBar.maxBtn.close()
        self.titleBar.closeBtn.hide()
        self.update()

        # 主题
        if self.theme == "Acrylic":
            if self.theme_color == "auto":
                # 自动
                if darkdetect.isDark():
                    # 亚克力 - 深色(自动)
                    self.windowEffect.setAcrylicEffect(self.winId(), "F2F2F230", False)
                else:
                    # 亚克力 - 浅色(自动)
                    self.windowEffect.setAcrylicEffect(self.winId(), "F2F2F230", False)
            elif self.theme_color == "dark":
                # 亚克力 - 深色
                self.windowEffect.setAcrylicEffect(self.winId(), "F2F2F230", False)
            else:
                # 亚克力 - 浅色
                self.windowEffect.setAcrylicEffect(self.winId(), "F2F2F230", False)
        else:
            # 玻璃
            self.windowEffect.setAeroEffect(self.winId())

        # 设置
        self.setupUi(self)
        # if not darkdetect.isDark():
        #     self.add_label.setStyleSheet('background:rgba(0,0,0,0);color:' + self.color_white + ";")
        #     self.clear_label.setStyleSheet('background:rgba(0,0,0,0);color:' + self.color_white + ";")
        #     self.text_color = self.color_white
        #     self.line_color = 0
        # self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.Tool)
        # self.setWindowFlags(QtCore.Qt.SplashScreen | QtCore.Qt.FramelessWindowHint)

        # 初始化托盘图标
        self.create_tray_icon()
        self.tray_icon.show()

        self.init_config()

        today_str = str(datetime.date.today().strftime("%Y-%m-%d"))
        drink_list = record_list.get_record_list()
        for drink in drink_list:
            if str(drink['date']) == str(today_str):
                self.schedule = int(drink['count'])

        # 强制关闭未关闭的使用线程
        util.thread_util.close_one_thread(self.time_thread)
        self.time_thread = time_thread.TimeThread(self.center_label)
        # 触发器
        self.time_thread.zero_trigger.connect(self.time_trigger_update)
        # 可以安全退出
        self.time_thread.setTerminationEnabled(True)
        self.time_thread.start()

    # 使用结束触发
    def time_trigger_update(self, end):
        today_str = str(datetime.date.today().strftime("%Y-%m-%d"))
        now_str = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        now = time.strptime(now_str, "%Y-%m-%d %H:%M:%S")
        self.time_add_count += 1
        if self.remind_interval == 0:
            return
        if self.time_add_count == self.remind_interval or (self.time_add_count % self.remind_interval) == 0:
            for active_time in self.active_time_list:
                if not active_time['active']:
                    continue
                start_time_str = today_str + " " + active_time['start_time'] + ":00"
                start_time = time.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
                end_time_str = today_str + " " + active_time['end_time'] + ":00"
                end_time = time.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")
                print(start_time_str)
                print(end_time_str)
                print(now_str)
                if start_time <= now <= end_time:
                    self.send_message(self.time_add_count)
                    return

    def init_config(self):
        drink_config = config.get_drink_config()
        self.remind_interval = int(drink_config['remind_interval'])
        self.drinking_count = int(drink_config['drinking_count'])
        self.view_message = drink_config['view_message']
        self.active_time_list = drink_config['active_time_list']
        self.view_top = drink_config['view_top']
        if self.view_top == "top":
            self.setWindowFlag(Qt.WindowStaysOnTopHint, True)       # 窗口置顶
        elif self.view_top == "under":
            self.setWindowFlag(Qt.WindowStaysOnBottomHint, True)    # 窗口置底
        self.show()

    # 创建托盘图标
    def create_tray_icon(self):
        menu = QMenu(self)
        menu.addAction(QAction(u'设置', self, triggered=self.open_setting_view))
        menu.addAction(QAction(u'刷新设置', self, triggered=self.refresh_setting))
        menu.addAction(QAction(u'历史记录', self, triggered=self.open_record_view))
        menu.addAction(QAction(u'退出', self, triggered=self.quit_before))
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.sys_icon)
        self.tray_icon.setContextMenu(menu)

    def push_button_add_click(self):
        self.schedule += 1
        self.time_add_count = 0
        record_list.set_record_list({
            "date": str(datetime.date.today().strftime("%Y-%m-%d")),
            "count": self.schedule
        })

    def push_button_clear_click(self):
        self.schedule = 0
        self.time_add_count = 0
        record_list.set_record_list({
            "date": str(datetime.date.today().strftime("%Y-%m-%d")),
            "count": self.schedule
        })

    '''
    **********************************鼠标事件 · 开始***************************************
    '''
    # 右键菜单
    def refresh_setting(self):
        self.init_config()

    # 右键菜单
    def open_right_button_menu(self):
        right_button_menu = QMenu()
        right_button_menu.addAction(QAction(u'设置', self, triggered=self.open_setting_view))
        right_button_menu.addAction(QAction(u'刷新设置', self, triggered=self.refresh_setting))
        right_button_menu.addAction(QAction(u'历史记录', self, triggered=self.open_record_view))
        right_button_menu.addAction(QAction(u'退出', self, triggered=self.quit_before))
        right_button_menu.exec_(QCursor.pos())

    # 打开设置界面
    def open_setting_view(self):
        self.setWindowFlag(Qt.WindowStaysOnTopHint, False)       # 窗口置顶
        self.show()
        self.setting_win = SettingWindow()
        self.setting_win.show()

    # 打开记录界面
    def open_record_view(self):
        self.setWindowFlag(Qt.WindowStaysOnTopHint, False)       # 窗口置顶
        self.show()
        self.record_win = RecordWindow()
        self.record_win.show()

    def send_message(self, time_count):
        with open('tmp.ico', 'wb') as tmp:
            tmp.write(base64.b64decode(icon.Icon().ig))
        print(str(os.getcwd()) + r"\tmp.ico")
        toast = Notification(app_id="Windows喝水记录工具",
                             title="喝水！！！",
                             msg="你已经" + str(time_count) + "分钟没有喝水了！快喝水！！！",
                             icon=str(os.getcwd()) + r"\tmp.ico")
        toast.show()
        time.sleep(2)
        os.remove("tmp.ico")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()    # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))          # 更改鼠标图标
        if event.button() == Qt.RightButton:
            self.open_right_button_menu()                       # 右键惨淡

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.m_flag:
            self.move(event.globalPos() - self.m_Position)      # 更改窗口位置
            event.accept()

    def mouseReleaseEvent(self, event):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
    '''
    **********************************鼠标事件 · 结束***************************************
    '''

    '''
    **********************************渲染 · 开始***************************************
    '''
    def paintEvent(self, event):
        # 绘制准备工作，启用反锯齿
        painter = QPainter(self)
        painter.setRenderHints(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.NoPen)
        background_arc_gradient = QConicalGradient(50, 50, 91)
        background_arc_gradient.setColorAt(0, QColor(self.line_color, self.line_color, self.line_color, 50))
        background_arc_gradient.setColorAt(1, QColor(self.line_color, self.line_color, self.line_color, 50))
        self.background_arc_pen = QPen()
        self.background_arc_pen.setBrush(background_arc_gradient)  # 设置画刷渐变效果
        self.background_arc_pen.setWidth(8)
        self.background_arc_pen.setCapStyle(Qt.RoundCap)
        painter.setPen(self.background_arc_pen)
        painter.drawArc(QtCore.QRectF(40, 40, 110, 110), 0, 360*16)  # 画外圆
        gradient = QConicalGradient(50, 50, 91)
        gradient.setColorAt(0, QColor(self.text_color))
        gradient.setColorAt(1, QColor(self.text_color))
        self.pen = QPen()
        self.pen.setBrush(gradient)  # 设置画刷渐变效果
        self.pen.setWidth(8)
        self.pen.setCapStyle(Qt.RoundCap)
        painter.setPen(self.pen)
        rotate_angle = 360 * self.schedule / self.drinking_count
        painter.drawArc(QtCore.QRectF(40, 40, 110, 110), (90 - 0) * 16, int(-rotate_angle * 16))  # 画圆环

        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(13)
        painter.setFont(font)
        painter.setPen(QColor(self.text_color))
        if self.view_message == "positive":
            painter.drawText(QtCore.QRectF(0, 0, 195, 35), Qt.AlignCenter,
                             "今天第%d杯水" % self.schedule)  # 显示进度条当前进度(正着数)
        else:
            if int(self.drinking_count - self.schedule) > 0:
                painter.drawText(QtCore.QRectF(0, 0, 195, 35), Qt.AlignCenter,
                                 "还有%d杯水" % int(self.drinking_count - self.schedule))  # 显示进度条当前进度(倒着数)
            elif int(self.drinking_count - self.schedule) == 0:
                painter.drawText(QtCore.QRectF(0, 0, 195, 35), Qt.AlignCenter,
                                 "%d杯水目标完成" % int(self.drinking_count))  # 显示进度条当前进度(倒着数)
            else:
                painter.drawText(QtCore.QRectF(0, 0, 195, 35), Qt.AlignCenter,
                                 "今天第%d杯水" % self.schedule)  # 显示进度条当前进度(正着数)

        self.update()
    '''
    **********************************渲染 · 结束***************************************
    '''

    def quit_before(self):
        util.thread_util.close_one_thread(self.time_thread)                  # 使用
        QApplication.instance().quit()

    # 关闭事件
    def closeEvent(self, event):
        self.setVisible(False)                                  # 托盘图标会自动消失
        QtWidgets.qApp.quit()


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
