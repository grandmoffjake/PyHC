# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/thejake/Documents/python/PyHC/mainForm.ui'
#
# Created: Tue Mar  6 01:37:13 2012
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.w = QtGui.QWidget(MainWindow)
        self.w.setObjectName(_fromUtf8("w"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.w)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.m = QtGui.QHBoxLayout()
        self.m.setObjectName(_fromUtf8("m"))
        self.glFrame = QtGui.QGroupBox(self.w)
        self.glFrame.setTitle(_fromUtf8(""))
        self.glFrame.setObjectName(_fromUtf8("glFrame"))
        self.verticalLayout = QtGui.QVBoxLayout(self.glFrame)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.vLayout = QtGui.QVBoxLayout()
        self.vLayout.setObjectName(_fromUtf8("vLayout"))
        self.verticalLayout.addLayout(self.vLayout)
        self.m.addWidget(self.glFrame)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.m.addItem(spacerItem)
        self.dialsContainer = QtGui.QGroupBox(self.w)
        self.dialsContainer.setMaximumSize(QtCore.QSize(150, 16777215))
        self.dialsContainer.setTitle(_fromUtf8(""))
        self.dialsContainer.setObjectName(_fromUtf8("dialsContainer"))
        self.verticalLayoutWidget = QtGui.QWidget(self.dialsContainer)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 20, 151, 561))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.dialsLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.dialsLayout.setMargin(0)
        self.dialsLayout.setObjectName(_fromUtf8("dialsLayout"))
        self.myDial = QtGui.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(150)
        sizePolicy.setHeightForWidth(self.myDial.sizePolicy().hasHeightForWidth())
        self.myDial.setSizePolicy(sizePolicy)
        self.myDial.setMinimumSize(QtCore.QSize(0, 150))
        self.myDial.setText(_fromUtf8(""))
        self.myDial.setObjectName(_fromUtf8("myDial"))
        self.dialsLayout.addWidget(self.myDial)
        self.m.addWidget(self.dialsContainer)
        self.verticalLayout_2.addLayout(self.m)
        MainWindow.setCentralWidget(self.w)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

