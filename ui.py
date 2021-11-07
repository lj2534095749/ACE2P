import os
import sys

from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QHBoxLayout, QVBoxLayout, QFileDialog, QLabel

from hairdressing import Ace2p

import _thread

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()  # 初始化UI
        self.initValue()  # 初始化值

    def initUI(self):
        self.setWindowTitle("CV Group 9 美发")  # 设置窗口标题
        self.resize(1800, 960)  # 设置窗口大小

        self.menubar = self.menuBar()  # 创建一个菜单栏
        self.mainMenu = self.menubar.addMenu("系统菜单")  # 添加菜单

        self.selectImageAction = QAction(QIcon('exit.png'), '&选择图片', self)
        self.selectImageAction.setShortcut('Ctrl+D')
        self.selectImageAction.setStatusTip('选择图片')
        self.selectImageAction.triggered.connect(self.openImage)
        self.mainMenu.addAction(self.selectImageAction)

        self.putResultAction = QAction(QIcon('exit.png'), '&生成结果', self)
        self.putResultAction.setShortcut('Ctrl+F')
        self.putResultAction.setStatusTip('生成结果')
        self.putResultAction.triggered.connect(self.putResult)
        self.mainMenu.addAction(self.putResultAction)

        self.text0 = QLabel(self)
        self.text0.setFixedSize(400, 200)
        self.text0.setText(" CV 第9组\n 曹润琪（组长）\n 郭颖 李杰  廖鑫\n 刘文江 李奇伟  房敏营")
        self.text0.move(0, 60)
        self.text0.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{color:rgb(300,300,300,120);font-size:30px;font-weight:bold;font-family:宋体;}")

        self.label0 = QLabel(self)
        self.label0.setFixedSize(400, 300)
        self.label0.move(0, 360)
        self.label0.setStyleSheet("QLabel{background:white;}")

        self.label1 = QLabel(self)
        self.label1.setFixedSize(400, 300)
        self.label1.move(500, 160)
        self.label1.setStyleSheet("QLabel{background:white;}")

        self.label2 = QLabel(self)
        self.label2.setFixedSize(400, 300)
        self.label2.move(920, 160)
        self.label2.setStyleSheet("QLabel{background:white;}")

        self.label3 = QLabel(self)
        self.label3.setFixedSize(400, 300)
        self.label3.move(1340, 160)
        self.label3.setStyleSheet("QLabel{background:white;}")

        self.label4 = QLabel(self)
        self.label4.setFixedSize(400, 300)
        self.label4.move(500, 520)
        self.label4.setStyleSheet("QLabel{background:white;}")

        self.label5 = QLabel(self)
        self.label5.setFixedSize(400, 300)
        self.label5.move(920, 520)
        self.label5.setStyleSheet("QLabel{background:white;}")

        self.label6 = QLabel(self)
        self.label6.setFixedSize(400, 300)
        self.label6.move(1340, 520)
        self.label6.setStyleSheet("QLabel{background:white;}")

    def initValue(self):
        self.imgName = ""
        self.imgType = ""

    def openImage(self):
        self.imgPath, self.imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        self.imgName = os.path.basename(self.imgPath)
        jpg = QtGui.QPixmap(self.imgPath).scaled(self.label0.width(), self.label0.height())
        self.label0.setPixmap(jpg)

    def putResult1(self):
        try:
            _thread.start_new_thread(self.computerThread)
        except Exception:
            print(Exception)


    def putResult(self):
        if self.imgName == "":
            return

        ace2p = Ace2p()
        ace2p.hairdressing(self.imgName)

        self.file_dir = r"D:\MachineLearning\Code\ACE2P\output"
        for root, dirs, files in os.walk(self.file_dir):
            self.files = files

        jpg = QtGui.QPixmap(self.file_dir + '/' + files[0]).scaled(self.label1.width(), self.label1.height())
        self.label1.setPixmap(jpg)

        jpg = QtGui.QPixmap(self.file_dir + '/' + files[1]).scaled(self.label2.width(), self.label2.height())
        self.label2.setPixmap(jpg)

        jpg = QtGui.QPixmap(self.file_dir + '/' + files[2]).scaled(self.label3.width(), self.label3.height())
        self.label3.setPixmap(jpg)

        jpg = QtGui.QPixmap(self.file_dir + '/' + files[3]).scaled(self.label4.width(), self.label4.height())
        self.label4.setPixmap(jpg)

        jpg = QtGui.QPixmap(self.file_dir + '/' + files[4]).scaled(self.label5.width(), self.label5.height())
        self.label5.setPixmap(jpg)

        jpg = QtGui.QPixmap(self.file_dir + '/' + files[5]).scaled(self.label6.width(), self.label6.height())
        self.label6.setPixmap(jpg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
