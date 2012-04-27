# -*- coding: utf-8 -*-

"""
Module implementing dlgChooseMap.
"""

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature

from Ui_mapDialog import Ui_dlgChooseMap

import os
import sys
import glob

class dlgChooseMap(QDialog, Ui_dlgChooseMap):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.mainWindow = parent
        for infile in glob.glob( os.path.join(sys.path[0], 'maps',  '*.jpg' ) ):
            self.lstMaps.addItem( os.path.basename( infile ) )
        
    def setMap(self, map):
        self.updatePreview( map )
        items = self.lstMaps.findItems( map, QtCore.Qt.MatchExactly )
        if len(items):
            self.lstMaps.setCurrentItem( items[0] )
            self.lstMaps.scrollToItem( items[0] )
        return
        
    def updatePreview(self, map):
        MapFile = os.path.join(sys.path[0], 'maps', str(map))
        pixmap = QtGui.QPixmap()
        pixmap.load( MapFile )
        self.mapPreview.setPixmap( pixmap.scaledToWidth( self.mapPreview.width() ) )
        self.mapPreview.update()

        
    @pyqtSignature("")
    def on_buttonBox_accepted(self):
        self.mainWindow.board.prepareMap( str( self.lstMaps.currentItem().text() ) )
        self.mainWindow.board.updateGL()
    
    @pyqtSignature("QString")
    def on_lstMaps_currentTextChanged(self, currentText):
        self.updatePreview( currentText )
