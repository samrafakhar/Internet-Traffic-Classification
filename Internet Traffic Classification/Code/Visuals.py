import pyshark
import collections
import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,  QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
import sys
from Protocol import fillprotocollist, Protocol


def unique(list1, unique_list):
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Packet Descriptions"
        self.top = 100
        self.left = 100
        self.width = 500
        self.height = 400
        self.createwindow()
        #self.InitWindow()


    def createwindow(self):
        cap = pyshark.FileCapture('file.pcap')

        protocolList = []
        sourceList = []
        destList = []
        lengthList = []
        self.I = 0
        listofprotocols = []
        fillprotocollist(listofprotocols)

        for packet in cap:
            if packet.transport_layer is not None:
                sourceList.append(packet[packet.transport_layer].srcport)
                destList.append(packet[packet.transport_layer].dstport)
                found = False
                for p in listofprotocols:
                    if packet.transport_layer is not None and (packet[packet.transport_layer].srcport == p.portnumber or packet[packet.transport_layer].dstport == p.portnumber):
                        protocolList.append(p.protocol)
                        found = True
                if not found:
                    protocolList.append("Others")
                lengthList.append(packet.length)
                self.I = self.I + 1
        self.counter = collections.Counter(protocolList)
        self.unique_list = []
        unique(protocolList, self.unique_list)

        self.table = []
        for x in range(self.I):
            self.table.append(sourceList[x])
            self.table.append(destList[x])
            self.table.append(lengthList[x])
            self.table.append(protocolList[x])


    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.creatingTables()
        #self.showFullScreen()
        self.show()


    def creatingTables(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(self.I+1)
        self.tableWidget.setColumnCount(4)

        self.tableWidget.setItem(0, 0, QTableWidgetItem("Source"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("Destination"))
        self.tableWidget.setItem(0, 2, QTableWidgetItem("Length"))
        self.tableWidget.setItem(0, 3, QTableWidgetItem("Protocol"))


        k=0
        for i in range (1, self.I+1):
            for j in range (4):
                self.tableWidget.setItem(i, j, QTableWidgetItem(self.table[k]))
                k=k+1

        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.addWidget(self.tableWidget)
        self.setLayout(self.vBoxLayout)

    def displaypiechart(self):
        cmap = plt.get_cmap('Set3')
        plt.rcParams.update({'font.size': 7})
        colors = cmap(np.linspace(0, 1, len(self.unique_list)))
        labels = self.unique_list
        sizes = list(self.counter.values())
        patches, texts, autotexts = plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        for patch, txt in zip(patches, autotexts):
            ang = (patch.theta2 + patch.theta1) / 2.
            x = patch.r * 0.85 * np.cos(ang * np.pi / 180)
            y = patch.r * 0.85 * np.sin(ang * np.pi / 180)
            txt.set_position((x, y))
        plt.legend(patches, labels, loc="best")
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        mng = plt.get_current_fig_manager()
        #mng.window.state('zoomed')
        #plt.axis('equal')
        plt.show()

    def displaybargraph(self):
        cmap = plt.get_cmap('plasma')
        colours = cmap(np.linspace(0, 1, len(self.unique_list)))
        y_pos = np.arange(len(list(self.counter.keys())))
        plt.bar(y_pos, list(self.counter.values()), align='center', alpha=0.5, color=colours)
        plt.xticks(y_pos, list(self.counter.keys()))
        plt.ylabel("Frequency")
        plt.xlabel("Protocol Name")
        #mng = plt.get_current_fig_manager()
        #mng.window.state('zoomed')
        #plt.tight_layout()

        plt.show()

    def displayBrokenBarhGraph(self):
        perc = [i / self.I for i in self.counter.values()]
        percentage = [i * 100 for i in perc]
        percsum = []
        for x in range(0, len(percentage)):
            percsum.append(sum(percentage[:x]))
        percsum.append(100)

        touplee = []
        for x in range(0, len(percsum) - 1):
            touplee.append(tuple((percsum[x], percsum[x + 1])))
        touplee.append(tuple((percsum[len(percsum) - 1], 100)))

        fig, ax = plt.subplots()

        cmap = plt.get_cmap('Pastel1')
        colors = cmap(np.linspace(0, 1, len(self.unique_list)))

        ax.broken_barh(touplee, [10, 9], facecolors=colors)
        ax.set_ylim(5, 10)
        ax.set_xlim(0, 100)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_yticks([15, 25])
        ax.set_xticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

        ax.set_axisbelow(True)

        ax.set_yticklabels([' '])
        ax.grid(axis='x')
        print(percsum)
        i = 2
        y = 1
        for x in range(0, len(percsum) - 1):
            if round(percentage[x], 1) < 10.0:
                ax.text(percsum[y], 9 + i, str(round(percentage[x], 1)) + "%", fontsize=6, horizontalalignment='right')
                ax.text(percsum[y], 9 + i + 0.75, self.unique_list[x], fontsize=6, horizontalalignment='right')
                if i < 7:
                    i = i + 3
                else:
                    i = 1
            else:
                ax.text(percsum[y], 14.5, str(round(percentage[x], 1)) + "%", fontsize=6, horizontalalignment='right')
                ax.text(percsum[y], 14.5 + 0.75, self.unique_list[x], fontsize=6, horizontalalignment='right')
            if y < len(percsum) - 1:
                y = y + 1
        plt.suptitle('Percentage Breakdown of Captured Data', fontsize=16)
        plt.show()