# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/thejake/Documents/python/PyHC/mapDialog.ui'
#
# Created: Wed Mar 21 22:42:40 2012
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_dlgChooseMap(object):
    def setupUi(self, dlgChooseMap):
        dlgChooseMap.setObjectName(_fromUtf8("dlgChooseMap"))
        dlgChooseMap.setWindowModality(QtCore.Qt.ApplicationModal)
        dlgChooseMap.resize(558, 397)
        dlgChooseMap.setModal(True)
        self.buttonBox = QtGui.QDialogButtonBox(dlgChooseMap)
        self.buttonBox.setGeometry(QtCore.QRect(380, 350, 171, 32))
        self.buttonBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.lstMaps = QtGui.QListWidget(dlgChooseMap)
        self.lstMaps.setGeometry(QtCore.QRect(10, 10, 191, 331))
        self.lstMaps.setObjectName(_fromUtf8("lstMaps"))
        self.mapPreview = QtGui.QLabel(dlgChooseMap)
        self.mapPreview.setGeometry(QtCore.QRect(210, 10, 331, 331))
        self.mapPreview.setFrameShape(QtGui.QFrame.Box)
        self.mapPreview.setText(_fromUtf8(""))
        self.mapPreview.setObjectName(_fromUtf8("mapPreview"))

        self.retranslateUi(dlgChooseMap)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), dlgChooseMap.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), dlgChooseMap.reject)
        QtCore.QMetaObject.connectSlotsByName(dlgChooseMap)

    def retranslateUi(self, dlgChooseMap):
        dlgChooseMap.setWindowTitle(QtGui.QApplication.translate("dlgChooseMap", "Choose a Map", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    dlgChooseMap = QtGui.QDialog()
    ui = Ui_dlgChooseMap()
    ui.setupUi(dlgChooseMap)
    dlgChooseMap.show()
    sys.exit(app.exec_())

