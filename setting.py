# coding:utf-8
from qframelesswindow import AcrylicWindow
from setting_form import Ui_Form
from PyQt5 import QtCore, QtWidgets
import os
import config
import datetime
import base64
import icon.collection as collection
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QApplication, QDialog, QMessageBox, QPushButton,
                             QLabel, QCheckBox, QComboBox, QLineEdit, QSpinBox,
                             QMenu, QAction, QGridLayout, QHBoxLayout, QVBoxLayout,
                             QTextEdit, QGroupBox, QStyle, QSystemTrayIcon)


class SettingWindow(AcrylicWindow, Ui_Form):

    def __init__(self, parent=None):
        super(SettingWindow, self).__init__(parent=parent)

        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.Tool)

        # 设置标题栏
        self.setWindowTitle("Windows喝水记录工具")

        drink_config = config.get_drink_config()
        self.check_box_active_time_1.setChecked(drink_config['active_time_list'][0]['active'])
        self.check_box_active_time_2.setChecked(drink_config['active_time_list'][1]['active'])
        self.check_box_active_time_3.setChecked(drink_config['active_time_list'][2]['active'])
        start_time_1 = datetime.datetime.strptime(drink_config['active_time_list'][0]['start_time'] + ":00", "%H:%M:%S")
        self.date_time_edit_start_time_1.setTime(start_time_1.time())
        start_time_2 = datetime.datetime.strptime(drink_config['active_time_list'][1]['start_time'] + ":00", "%H:%M:%S")
        self.date_time_edit_start_time_2.setTime(start_time_2.time())
        start_time_3 = datetime.datetime.strptime(drink_config['active_time_list'][2]['start_time'] + ":00", "%H:%M:%S")
        self.date_time_edit_start_time_3.setTime(start_time_3.time())
        end_time_1 = datetime.datetime.strptime(drink_config['active_time_list'][0]['end_time'] + ":00", "%H:%M:%S")
        self.date_time_edit_end_time_1.setTime(end_time_1.time())
        end_time_2 = datetime.datetime.strptime(drink_config['active_time_list'][1]['end_time'] + ":00", "%H:%M:%S")
        self.date_time_edit_end_time_2.setTime(end_time_2.time())
        end_time_3 = datetime.datetime.strptime(drink_config['active_time_list'][2]['end_time'] + ":00", "%H:%M:%S")
        self.date_time_edit_end_time_3.setTime(end_time_3.time())
        self.spin_box_remind_interval.setValue(int(drink_config['remind_interval']))
        self.spin_box_drinking_count.setValue(int(drink_config['drinking_count']))
        view_message = drink_config['view_message']
        view_message_str = "正着计数" if view_message == "positive" else "倒着计数"
        self.combo_box_view_message.setCurrentText(view_message_str)
        view_top = drink_config['view_top']
        view_top_str = "正常" if view_top == "normal" else "置顶" if view_top == "top" else "置底"
        self.combo_box_view_top.setCurrentText(view_top_str)
        with open('collection.jpg', 'wb') as tmp:
            tmp.write(base64.b64decode(collection.Collection().ig))
            image_path = "collection.jpg"
            pic = QPixmap(image_path)
            pic = pic.scaled(int(pic.width() / 3), int(pic.height() / 3))
            label_pic = QLabel("show", self)
            label_pic.setPixmap(pic)
            label_pic.setGeometry(265, 50, 216, 336)
        os.remove("collection.jpg")

    def push_button_ok_click(self):
        view_message_str = self.combo_box_view_message.itemText(self.combo_box_view_message.currentIndex())
        view_message = "positive" if view_message_str == "正着计数" else "negative"
        view_top_str = self.combo_box_view_top.itemText(self.combo_box_view_top.currentIndex())
        view_top = "normal" if view_top_str == "正常" else "top" if view_top_str == "置顶" else "under"
        drink_config = {
            "active_time_list": [
                {
                    "active": self.check_box_active_time_1.isChecked(),
                    "start_time": str(self.date_time_edit_start_time_1.text()),
                    "end_time": str(self.date_time_edit_end_time_1.text())
                },
                {
                    "active": self.check_box_active_time_2.isChecked(),
                    "start_time": str(self.date_time_edit_start_time_2.text()),
                    "end_time": str(self.date_time_edit_end_time_2.text())
                },
                {
                    "active": self.check_box_active_time_3.isChecked(),
                    "start_time": str(self.date_time_edit_start_time_3.text()),
                    "end_time": str(self.date_time_edit_end_time_3.text())
                },
            ],
            "remind_interval": int(self.spin_box_remind_interval.text()),   # 间隔时间(分钟)
            "drinking_count": int(self.spin_box_drinking_count.text()),     # 喝水数量
            "view_message": view_message,                                   # 窗口信息 正着计数(positive)/倒着计数(negative)
            "view_top": view_top                                            # 窗口 置顶(top)/正常(normal)/置底(under)
        }
        config.set_drink_config(drink_config)
        self.label_message.setText("保存成功，请在回到主页面后右键->刷新设置，或在托盘处右键->刷新设置")
