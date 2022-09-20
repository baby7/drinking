import os
import sys
import base64
import icon.icon as icon
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton


# 打包命令
# pyinstaller -F -w -i D:\project\python\drinking\icon\favicon.ico main.py

class RoundProgress(QWidget):

    _startPos = None
    _endPos = None
    _isTracking = False
    pen = None
    background_arc_pen = None
    schedule = 0

    def __init__(self):
        super(RoundProgress, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)  # 去边框
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        # 设置图标
        with open('tmp.ico', 'wb') as tmp:
            tmp.write(base64.b64decode(icon.Icon().ig))
        self.setWindowIcon(QIcon('tmp.ico'))
        os.remove("tmp.ico")

        font_ui = QtGui.QFont()
        font_ui.setFamily("黑体")
        font_ui.setPointSize(45)
        font_ui.setBold(False)
        font_ui.setWeight(50)

        label = QLabel("🥛", self)
        label.move(73, 76)
        label.setFont(font_ui)

        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)

        self.clear_label = QPushButton(self)
        self.clear_label.setText("〇")
        self.clear_label.setMaximumWidth(25)
        self.clear_label.setMaximumHeight(25)
        self.clear_label.setFont(font)
        self.clear_label.setStyleSheet('QPushButton{background:rgba(0,0,0,0);color: #FFFFFF;}')
        op = QtWidgets.QGraphicsOpacityEffect()
        self.clear_label.setGraphicsEffect(op)
        self.clear_label.setAutoFillBackground(True)
        self.clear_label.move(180, 180)
        self.clear_label.clicked.connect(self.click_clear)

        self.add_label = QPushButton(self)
        self.add_label.setText("✚")
        self.add_label.setMaximumWidth(25)
        self.add_label.setMaximumHeight(25)
        self.add_label.setFont(font)
        self.add_label.setStyleSheet('QPushButton{background:rgba(0,0,0,0);color: #FFFFFF;}')
        op = QtWidgets.QGraphicsOpacityEffect()
        self.add_label.setGraphicsEffect(op)
        self.add_label.setAutoFillBackground(True)
        self.add_label.move(15, 180)
        self.add_label.clicked.connect(self.click_add)

        self.add_label = QPushButton(self)
        self.add_label.setText("×")
        self.add_label.setMaximumWidth(25)
        self.add_label.setMaximumHeight(25)
        self.add_label.setFont(font)
        self.add_label.setStyleSheet('QPushButton{background:rgba(0,0,0,0);color: #FFFFFF;}')
        op = QtWidgets.QGraphicsOpacityEffect()
        self.add_label.setGraphicsEffect(op)
        self.add_label.setAutoFillBackground(True)
        self.add_label.move(180, 15)
        self.add_label.clicked.connect(QCoreApplication.instance().quit)

        label_none = QLabel("", self)
        label_none.move(500, 500)

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

    def parameterUpdate(self, p):
        self.schedule = p

    def paintEvent(self, event):
        # 绘制准备工作，启用反锯齿
        painter = QPainter(self)
        painter.setRenderHints(QtGui.QPainter.Antialiasing)

        painter.setPen(QtCore.Qt.NoPen)

        painter.setBrush(QBrush(QColor(0, 0, 0, 100)))
        painter.drawRoundedRect(0, 0, 225, 225, 10, 10)  # 画圆角矩形背景

        painter.setBrush(QBrush(QColor(95, 137, 255, 255)))

        background_arc_gradient = QConicalGradient(50, 50, 91)
        background_arc_gradient.setColorAt(0, QColor(255, 255, 255, 50))
        background_arc_gradient.setColorAt(1, QColor(255, 255, 255, 50))
        self.background_arc_pen = QPen()
        self.background_arc_pen.setBrush(background_arc_gradient)  # 设置画刷渐变效果
        self.background_arc_pen.setWidth(8)
        self.background_arc_pen.setCapStyle(Qt.RoundCap)
        painter.setPen(self.background_arc_pen)
        painter.drawArc(QtCore.QRectF(38, 50, 149, 149), 0, 360*16)  # 画外圆

        gradient = QConicalGradient(50, 50, 91)
        gradient.setColorAt(0, QColor("#FFFFFF"))
        gradient.setColorAt(1, QColor("#FFFFFF"))
        self.pen = QPen()
        self.pen.setBrush(gradient)  # 设置画刷渐变效果
        self.pen.setWidth(8)
        self.pen.setCapStyle(Qt.RoundCap)
        painter.setPen(self.pen)
        rotate_angle = 360 * self.schedule / 8
        painter.drawArc(QtCore.QRectF(38, 50, 149, 149), (90 - 0) * 16, int(-rotate_angle * 16))  # 画圆环

        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(13)
        painter.setFont(font)
        painter.setPen(QColor("#FFFFFF"))
        painter.drawText(QtCore.QRectF(0, 0, 225, 50), Qt.AlignCenter, "今天第%d杯水" % self.schedule)  # 显示进度条当前进度
        self.update()

    def click_clear(self):
        self.schedule = 0

    def click_add(self):
        self.schedule += 1


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    RoundProgress = RoundProgress()
    RoundProgress.show()
    sys.exit(app.exec_())
