# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PokerGameGUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys
sys.path.append("..")
from deckClass import Deck
from playerClass import Player
from smarterPlayer import smarterPlayer
from interactivePlayer import interactivePlayer
from interactiveGUIPlayer import  interactiveGUIPlayer
from PokerTableClass import table

import io

from io import StringIO

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


class Ui_MainWindow(object):

    def __init__(self):
        super(Ui_MainWindow, self).__init__()

        self.aTable = None
        self.MAX_ITERATION = 100
        self.PlayerList = []

        self.action = None
        self.bet = 0

        self.f = io.StringIO()

        self.agent = None




    def callClicked(self):
        self.action = 'CALL'
        self.communityCards.append(self.action)
        self.agent.setBet(self.bet)
        self.agent.setAction('CALL')
        self.agent.setWait()

    def foldClicked(self):
        self.action = 'FOLD'
        self.communityCards.append(self.action)
        self.agent.setBet(self.bet)
        self.agent.setAction('FOLD')
        self.agent.setWait()

    def betClicked(self):
        self.action = 'BET'
        self.communityCards.append(self.action)
        self.agent.setBet(self.bet)
        self.agent.setAction('BET')
        self.agent.setWait()

    def valuechange(self):
        """
        function to capture Qslide value
        Returns
        -------
        """
        self.bet = self.betSize.value()
        self.communityCards.append(str(self.bet))

    def startClicked(self):
        with Capturing() as output:
            self.gameEngine()

        self.playerHands.append(str(output))

    def gameEngine(self):

        print("TEST TEST TEST")

        p1 = Player("p1")
        p2 = Player("p2")
        p3 = Player("p3")
        p4 = Player("p4")
        p5 = interactivePlayer("ip5")
        p6 = smarterPlayer("sp6")

        self.agent = p5

        aTable = table()
        aTable.setMaxGames(1000)

        aTable.addPlayer(p1, 100)
        aTable.addPlayer(p2, 100)
        aTable.addPlayer(p3, 100)
        aTable.addPlayer(p4, 100)
        aTable.addPlayer(p5, 100)
        aTable.addPlayer(p6, 100)

        print("Table Setted up with Six dummy player")
        print("Number of Players " + str(aTable.getNPlayer()))
        print("Number of Active Players " + str(aTable.getNPlayer_active()))
        print("Number of inGame Players " + str(aTable.getNPlayer_inGame()))

        aTable.runGame()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(782, 624)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.CALL = QtWidgets.QPushButton(self.centralwidget)
        self.CALL.setGeometry(QtCore.QRect(60, 350, 141, 51))
        self.CALL.setObjectName("CALL")
        self.BET = QtWidgets.QPushButton(self.centralwidget)
        self.BET.setGeometry(QtCore.QRect(60, 410, 141, 51))
        self.BET.setObjectName("BET")
        self.FOLD = QtWidgets.QPushButton(self.centralwidget)
        self.FOLD.setGeometry(QtCore.QRect(60, 470, 141, 51))
        self.FOLD.setObjectName("FOLD")
        self.betSize = QtWidgets.QSlider(self.centralwidget)
        self.betSize.setGeometry(QtCore.QRect(220, 350, 31, 171))
        self.betSize.setOrientation(QtCore.Qt.Vertical)
        self.betSize.setObjectName("betSize")
        self.playerHands = QtWidgets.QTextBrowser(self.centralwidget)
        self.playerHands.setGeometry(QtCore.QRect(260, 350, 461, 171))
        self.playerHands.setObjectName("playerHands")
        self.communityCards = QtWidgets.QTextBrowser(self.centralwidget)
        self.communityCards.setGeometry(QtCore.QRect(60, 130, 661, 192))
        self.communityCards.setObjectName("communityCards")
        self.Start = QtWidgets.QPushButton(self.centralwidget)
        self.Start.setGeometry(QtCore.QRect(610, 20, 111, 101))
        self.Start.setObjectName("Start")
        self.PlayerType = QtWidgets.QComboBox(self.centralwidget)
        self.PlayerType.setGeometry(QtCore.QRect(340, 20, 131, 41))
        self.PlayerType.setObjectName("PlayerType")
        self.PlayerType.addItem("")
        self.PlayerType.addItem("")
        self.AddPlayer = QtWidgets.QPushButton(self.centralwidget)
        self.AddPlayer.setGeometry(QtCore.QRect(490, 20, 111, 101))
        self.AddPlayer.setObjectName("AddPlayer")
        self.StackSize = QtWidgets.QComboBox(self.centralwidget)
        self.StackSize.setGeometry(QtCore.QRect(340, 80, 131, 41))
        self.StackSize.setObjectName("StackSize")
        self.StackSize.addItem("")
        self.StackSize.addItem("")
        self.StackSize.addItem("")
        self.CreateTable = QtWidgets.QPushButton(self.centralwidget)
        self.CreateTable.setGeometry(QtCore.QRect(60, 80, 131, 41))
        self.CreateTable.setObjectName("CreateTable")
        self.MAXIteration = QtWidgets.QComboBox(self.centralwidget)
        self.MAXIteration.setGeometry(QtCore.QRect(60, 20, 131, 41))
        self.MAXIteration.setObjectName("MAXIteration")
        self.MAXIteration.addItem("")
        self.MAXIteration.addItem("")
        self.MAXIteration.addItem("")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 782, 21))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        ##### user defined actions:
        self.CALL.clicked.connect(self.callClicked)
        self.BET.clicked.connect(self.betClicked)
        self.FOLD.clicked.connect(self.foldClicked)

        ##### Qslide for betsize
        self.betSize.setMinimum(0)
        self.betSize.setMaximum(100)
        self.betSize.setValue(0)
        self.betSize.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.betSize.setTickInterval(5)
        self.betSize.valueChanged.connect(self.valuechange)

        ##### textBrowser
        self.playerHands.append(self.f.getvalue())

        ##### run Game
        self.Start.clicked.connect(self.startClicked)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.CALL.setText(_translate("MainWindow", "CALL"))
        self.BET.setText(_translate("MainWindow", "BET"))
        self.FOLD.setText(_translate("MainWindow", "FOLD"))
        self.Start.setText(_translate("MainWindow", "Start"))
        self.PlayerType.setItemText(0, _translate("MainWindow", "DummyPlayer"))
        self.PlayerType.setItemText(1, _translate("MainWindow", "SmartPlayer"))
        self.AddPlayer.setText(_translate("MainWindow", "Add Player"))
        self.StackSize.setItemText(0, _translate("MainWindow", "100"))
        self.StackSize.setItemText(1, _translate("MainWindow", "200"))
        self.StackSize.setItemText(2, _translate("MainWindow", "300"))
        self.CreateTable.setText(_translate("MainWindow", "Create Table"))
        self.MAXIteration.setItemText(0, _translate("MainWindow", "100 Games"))
        self.MAXIteration.setItemText(1, _translate("MainWindow", "500 Games"))
        self.MAXIteration.setItemText(2, _translate("MainWindow", "1000 Games"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
