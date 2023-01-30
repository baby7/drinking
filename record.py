# coding:utf-8
from PyQt5.QtCore import Qt
from qframelesswindow import AcrylicWindow
from record_form import Ui_Form
from PyQt5 import QtCore

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import record_list


class RecordWindow(AcrylicWindow, Ui_Form):

    def __init__(self, parent=None):
        super(RecordWindow, self).__init__(parent=parent)

        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.Tool)

        # 设置标题栏
        self.setWindowTitle("Windows喝水记录工具")
        # drink_list = [
        #     {
        #         "date": "2023-01-28",
        #         "count": 1
        #     },
        #     {
        #         "date": "2023-01-29",
        #         "count": 2
        #     },
        # ]
        drink_list = record_list.get_record_list()
        write_table_view(self.drink_table_view, drink_list,
                         ['日期', '杯数'], ['date', 'count'])
        self.drink_table_view.setColumnWidth(0, 100)
        self.drink_table_view.setColumnWidth(1, 40)


# 渲染列表
def write_table_view(table_view, data_list, title_list, name_list):
    model = QStandardItemModel(len(data_list), len(name_list))
    model.setHorizontalHeaderLabels(title_list)
    for row in range(len(data_list)):
        for line in range(len(name_list)):
            model.setItem(row, line, QStandardItem(str(data_list[row][name_list[line]])))
    table_view.setModel(model)
    # 设置滚动条
    table_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    # 设置表头不可点击
    table_view.horizontalHeader().setSectionsClickable(False)
    table_view.verticalHeader().setSectionsClickable(False)
    # 设置禁止编辑
    table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
    # 设置只能选中一行
    table_view.setSelectionMode(QAbstractItemView.SingleSelection)
    # 设置只能选中整行
    table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
    # 行高
    table_view.verticalHeader().setDefaultSectionSize(15)
