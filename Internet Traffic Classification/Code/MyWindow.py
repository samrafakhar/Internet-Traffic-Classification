from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import subprocess, time, signal, sys, os
from Visuals import Window
import pyshark


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.setGeometry(200, 200, 400, 300)
        self.setWindowTitle("Internet Traffic Classifier")
        self.initUI()

    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Welcome to the Internet Traffic Classifier")
        self.label.setStyleSheet("font: 75 14pt \"MS Shell Dlg 2\";")
        self.label.adjustSize()
        self.label.move(40, 60)
        self.btn1 = QtWidgets.QPushButton(self)
        self.btn1.clicked.connect(self.clickedstart)
        self.btn1.setText("Start Capturing")
        self.btn1.setStyleSheet("background:rgb(0, 170, 0);font: 75 14pt \"MS Shell Dlg 2\";")
        self.btn1.setGeometry(200, 200, 201, 61)
        self.btn1.move(100, 180)
        self.btn2 = QtWidgets.QPushButton(self)
        self.btn2.clicked.connect(self.clickedstop)
        self.btn2.setText("Stop Capturing")
        self.btn2.setStyleSheet("background:red;font: 75 14pt \"MS Shell Dlg 2\";")
        self.btn2.setGeometry(200, 200, 201, 61)
        self.btn2.move(100, 180)
        self.btn2.hide()

    def clickedstart(self):
        self.btn1.hide()
        self.btn2.show()
        self.p = subprocess.Popen(['windump', '-i', '2', '-w', 'file.pcap'], shell=True)

    def clickedstop(self):
        subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.p.pid)])
        #self.details = Window()
        self.btn2.hide()
        self.newwindow = Window()
        self.btn3 = QtWidgets.QPushButton(self)
        self.btn3.clicked.connect(self.gettable)
        self.btn3.setText("Show results in table")
        self.btn3.setStyleSheet("background:#F9E1A2;font: 75 14pt \"MS Shell Dlg 2\";")
        self.btn3.setGeometry(200, 200, 301, 31)
        self.btn3.move(50, 140)
        self.btn3.show()
        self.btn4 = QtWidgets.QPushButton(self)
        self.btn4.clicked.connect(self.getpiechart)
        self.btn4.setText("Display Pie Chart")
        self.btn4.setStyleSheet("background:#F9E1A2;font: 75 14pt \"MS Shell Dlg 2\";")
        self.btn4.setGeometry(200, 200, 301, 31)
        self.btn4.move(50, 175)
        self.btn4.show()
        self.btn5 = QtWidgets.QPushButton(self)
        self.btn5.clicked.connect(self.getbargraph)
        self.btn5.setText("Display Bar Graph")
        self.btn5.setStyleSheet("background:#F9E1A2;font: 75 14pt \"MS Shell Dlg 2\";")
        self.btn5.setGeometry(200, 200, 301, 31)
        self.btn5.move(50, 210)
        self.btn5.show()

        self.btn6 = QtWidgets.QPushButton(self)
        self.btn6.clicked.connect(self.getbrokenbarhgraph)
        self.btn6.setText("Display Percentage Bar Graph")
        self.btn6.setStyleSheet("background:#F9E1A2;font: 75 14pt \"MS Shell Dlg 2\";")
        self.btn6.setGeometry(200, 200, 301, 31)
        self.btn6.move(50, 245)
        self.btn6.show()



    def gettable(self):
        self.newwindow.InitWindow()

    def getpiechart(self):
        self.newwindow.displaypiechart()

    def getbargraph(self):
        self.newwindow.displaybargraph()

    def getbrokenbarhgraph(self):
        self.newwindow.displayBrokenBarhGraph()


app = QApplication(sys.argv)
win = MyWindow()
win.show()
sys.exit(app.exec())