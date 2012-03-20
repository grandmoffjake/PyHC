# -*- coding: utf-8 -*-
#TODO: Standies images/current click (interesting texture problem)
#TODO: Remove object/figure button
#TODO: Restore removed object/figure
#TODO: Click to move map functionality
#TODO: Hotkeys for predefined locations
#TODO: Hotkeys for terrain tokens/lof/object mode
#TODO: Map chooser
#TODO: Refactor dial images to read from XML definition
#TODO: XML Team abilities
#TODO: Netcode
#TODO: Team builder
#TODO: Graphics for buttons
#TODO: Fix width on dial pane (again)
#TODO: Fix transparency on images
#TODO: HTML dial code to XML dial code converter
#TODO: Build XML sets
#TODO: Feats and ATAs
#TODO: Multi-based figures
#TODO: Bystander Tokens

"""
Module implementing MainWindow.
"""
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMainWindow,  QApplication
from PyQt4.QtCore import pyqtSignature

from Ui_mainForm import Ui_MainWindow

from GameBoard import *

import math
import random
from ObjectSimpleSquare import *
from lxml import etree

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        
        self.mousePosition = [0, 0]
        self.MainWindow = MainWindow
        self.setupUi(self)
        self.show()

        self.glFrame.setTitle( " " )
        self.board = GameBoard(MainWindow, self)
        self.vLayout.addWidget(self.board)
        self.gameLog.keyPressEvent = self.test
        self.keyPressEvent = self.test
        self.board.wheelEvent = self.zoomMap
        self.board.mouseMoveEvent = self.moveMap
        self.board.mouseDoubleClickEvent = self.doubleClickMap
        self.board.mousePressEvent = self.clickMap
        self.board.mouseReleaseEvent = self.stopMoving
        self.lastX = False
        self.lastY = False
        self.mode = "team"
        
        self.myActiveClix = False
        self.theirActiveClix = False
        
        self.activeObject = False
        
        self.myDial.setMouseTracking(True)
#        self.myDial.mouseMoveEvent = self.hoverMyDial

    
    @pyqtSignature("")
    def on_actionChoose_Map_activated(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSignature("")
    def on_cmdBarrier_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.cmdBarrier.isChecked():
            self.clearOtherToggles( self.cmdBarrier )
            self.glFrame.setTitle( "Click a square with no figure in it to add a barrier token" )
        else:
            self.glFrame.setTitle( " " )

    def test(self,event):
        if self.mode == "team":
            return
            
        #print event.key()
        if event.key() == QtCore.Qt.Key_Up and self.board.view_angle_x < 90:
            self.board.view_angle_x += 1.0
            self.board.updateGL()
        elif event.key() == QtCore.Qt.Key_Down and self.board.view_angle_x > 20:
            self.board.view_angle_x -= 1.0
            self.board.updateGL()
        elif event.key() == QtCore.Qt.Key_Left:
            self.board.view_angle_y += 1.0
            self.board.updateGL()
        elif event.key() == QtCore.Qt.Key_Right:
            self.board.view_angle_y -= 1.0
            self.board.updateGL()
        elif event.key() == 87:
            self.board.y_pos += 1.0
            self.board.updateGL()
        elif event.key() == 83:
            self.board.y_pos -= 1.0
            self.board.updateGL()
        elif event.key() == 65:
            self.board.x_pos -= 1.0
            self.board.updateGL()
        elif event.key() == 68:
            self.board.x_pos += 1.0
            self.board.updateGL()
        elif event.key() == 81:
            self.board.z_pos -= 1.0
            self.board.updateGL()
        elif event.key() == 69:
            self.board.z_pos += 1.0
            self.board.updateGL()
        elif event.key() == 48:
            self.board.z_pos = 0.0
            self.board.y_pos = 0.0
            self.board.x_pos = 0.0
            self.board.view_angle_x = 90
            self.board.view_angle_y = 0
            self.board.view_distance = 1
            self.board.updateGL()
            '''
            if keystate[K_UP] and view_angle_x < 90:  view_angle_x += 1.0
            if keystate[K_DOWN] and view_angle_x > 0:  view_angle_x -= 1.0
            if keystate[K_LEFT]:  view_angle_y += 1.0
            if keystate[K_RIGHT]:  view_angle_y -= 1.0
            if keystate[K_PAGEUP] and view_distance < 2.0:  view_distance += .03
            if keystate[K_PAGEDOWN] and view_distance > 0.5:  view_distance -= .03
            if keystate[K_END]:  view_distance = 1.0;  view_angle_y = 0.0;  view_angle_x = 90.0
            '''
        else:
            return QtGui.QMainWindow.keyPressEvent(self.MainWindow, event)
    
    @pyqtSignature("")
    def on_cmdLOF_clicked(self):
        if self.cmdLOF.isChecked():
            self.board.modeLOF = True
            self.clearOtherToggles( self.cmdLOF )
        else:
            self.board.modeLOF = False
            self.glFrame.setTitle( " " )
            self.board.moving = False
            self.board.updateGL()
    
    @pyqtSignature("")
    def on_cmdObj_clicked(self):
        if self.cmdObj.isChecked():
            self.board.modeObject = True
            self.clearOtherToggles( self.cmdObj )
        else:
            self.board.modeObject = False
            self.glFrame.setTitle( " " )
            self.board.moving = False
            self.board.updateGL()
    
    @pyqtSignature("")
    def on_cmdStandies_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSignature("")
    def on_cmdRemoveObject_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSignature("")
    def on_cmdSmokeCloud_clicked(self):
        if self.cmdSmokeCloud.isChecked():
            self.clearOtherToggles( self.cmdSmokeCloud )
            self.glFrame.setTitle( "Click a square with no figure in it to add a smoke cloud token" )
        else:
            self.glFrame.setTitle( " " )
    
    @pyqtSignature("")
    def on_cmdDebris_clicked(self):
        if self.cmdDebris.isChecked():
            self.clearOtherToggles( self.cmdDebris )
            self.glFrame.setTitle( "Click a square with no figure in it to add a debris token" )
        else:
            self.glFrame.setTitle( " " )
    
    @pyqtSignature("")
    def on_cmdSpecial_clicked(self):
        if not self.cmdSpecial.isChecked():
            self.clearOtherToggles( self.cmdSpecial )
            self.glFrame.setTitle( "Click a square with no figure in it to add a special token" )
        else:
            self.glFrame.setTitle( " " )
    
    @pyqtSignature("")
    def on_rollTwo_clicked(self):
        v = random.randint( 2,  12 )
        s = "Rolled a "+str(v)+" on two dice."
        if v == 2:
            s += "  <b>Crit miss!</b>"
        elif v == 12:
            s += "  <b>Critical hit!</b>"
        self.board.log( "Me",  s )
    
    @pyqtSignature("")
    def on_rollOne_clicked(self):
        v = random.randint( 1,  6 )
        self.board.log( "Me",  "Rolled a "+str(v)+" on one die.")
    
    @pyqtSignature("")
    def on_cmdHeal_clicked(self):
        f = self.getMyActiveClix()
        if f:
            f.heal()
            self.redrawMyDial()
    
    @pyqtSignature("")
    def on_cmdTokenBlue_clicked(self):
        f = self.getMyActiveClix()
        if f:
            f.token( "blue" )
            self.board.updateGL()
    
    @pyqtSignature("")
    def on_cmdTokenRed_clicked(self):
        f = self.getMyActiveClix()
        if f:
            f.token( "red" )
            self.board.updateGL()
    
    @pyqtSignature("")
    def on_cmdDamage_clicked(self):
        f = self.getMyActiveClix()
        if f:
            f.damage()
            self.redrawMyDial()
        
        
    def getMyActiveClix(self):
        c = self.myActiveClix
        if c:
            x,  y = c
            f = self.board.boardFigures[x][y]
            if f:
                return f
                
        return False
                
    def getBoardXY(self, event):
        v = self.board.viewport()
        winY = v[3] - event.y()
        winX = event.x()
        winZ = self.board.getMouseZ(winX, winY)
        posX, posY, posZ = gluUnProject(winX, winY, winZ)

        x = int(math.ceil(posX)+11)
        y = int(math.ceil(posZ)+11)
        
        return [x, y]
        
    def hoverMyDial(self, event):
        if self.myActiveClix:
            f = self.board.boardFigures[self.myActiveClix[0]][self.myActiveClix[1]]
            if f:
                t = f.getToolTip(event.pos())
                if t:
                    QtGui.QToolTip.showText( event.globalPos(),  "<p>"+t+"</p>",  self.myDial )
                else:
                    QtGui.QToolTip.hideText()
        
    def clickMap(self, event):
        x,  y = self.getBoardXY(event)
        if ( x >= 0 and x <= 23 and y >= 0 and y <= 23 ):
            if event.button() == QtCore.Qt.RightButton and self.board.boardObjects[x][y]:
                #Picking up an object
                o = self.board.boardObjects[x][y]
                f = False
                if self.myActiveClix:
                    f = self.board.boardFigures[self.myActiveClix[0]][self.myActiveClix[1]]
                
                if o and o.canBePickedUp() and f:
                    b = f.takeObject(o)
                    if b:
                        self.board.updateGL()
                elif isinstance(o, ObjectSimpleSquare):
                    if o.type == "barrier":
                        o.type = "debris"
                        if f:
                            self.board.log( "Me",  f.getName() + " destroys a square of blocking terrain." )
                        else:
                            self.board.log( "Me",  "Destroyed a square of blocking terrain.")
                    else:
                        self.board.boardObjects[x][y] = False
                        self.board.log( "Me",  "Removed a square of "+o.type+" terrain.")
                        
                    self.board.updateGL()
            elif event.button() == QtCore.Qt.RightButton and self.board.boardFigures[x][y] and self.board.boardFigures[x][y].hasObject() and self.board.boardFigures[x][y].mine:
                #Dropping an object
                f = self.board.boardFigures[x][y]
                f.dropObject()
                self.myActiveClix = (x, y)
                self.board.updateGL()
            elif (self.cmdBarrier.isChecked() or self.cmdSmokeCloud.isChecked() or self.cmdDebris.isChecked() or self.cmdSpecial.isChecked()) and not self.board.boardObjects[x][y]:
                if self.cmdBarrier.isChecked():
                    type = "barrier"
                elif self.cmdSmokeCloud.isChecked():
                    type = "smoke cloud"
                elif self.cmdDebris.isChecked():
                    type = "debris"
                elif self.cmdSpecial.isChecked():
                    type = "special"
                    
                b = ObjectSimpleSquare(self.board, type)
                self.board.boardObjects[x][y] = b
                b.x = x
                b.y = y
                self.board.log( "Me",  "Placed a "+type+" token." )
                self.board.updateGL()
            else:
                if ( self.board.boardFigures[x][y] and not self.board.modeObject ):
                    f = self.board.boardFigures[x][y]
                    self.board.moving = True
                    self.board.moveOriginX = self.board.moveDestinationX = x
                    self.board.moveOriginY = self.board.moveDestinationY = y
                    
                    #self.board.clearMyActive()
                    if f.mine:
                        self.board.clearActive(1)
                        self.myActiveClix = (x, y)
                        f.active = 1
                        self.redrawMyDial()
                    else:
                        self.board.clearActive(2)
                        self.theirActiveClix = (x, y)
                        f.active = 2
                        self.redrawTheirDial()
                elif self.board.boardObjects[x][y]:
                    self.board.moving = True
                    self.board.modeObject = True
                    self.board.moveOriginX = self.board.moveDestinationX = x
                    self.board.moveOriginY = self.board.moveDestinationY = y
                    
                    self.activeObject = (x, y)
                    self.redrawMyDial()
                elif self.cmdLOF.isChecked():
                    self.board.moving = True
                    self.board.moveOriginX = self.board.moveDestinationX = x
                    self.board.moveOriginY = self.board.moveDestinationY = y
                
    def redrawMyDial(self):
        if self.board.modeObject:
            f = self.board.boardObjects[self.activeObject[0]][self.activeObject[1]]
        else:
            f = self.board.boardFigures[self.myActiveClix[0]][self.myActiveClix[1]]
        if f:
            png = f.drawDial()
            if png:
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(png, "PNG")
                self.myDial.setPixmap( pixmap )
                self.myDial.update()
        
    def redrawTheirDial(self):
        f = self.board.boardFigures[self.theirActiveClix[0]][self.theirActiveClix[1]]
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(f.drawDial(), "PNG")
        self.theirDial.setPixmap( pixmap )
        self.theirDial.update()
        
    def doubleClickMap(self, event):
        x, y = self.getBoardXY(event)
        #print  "X %s Y %s aX %s aY %s vD %s Xoffset %s Yoffset %s Zoffset %s" % ( x,  y,  self.board.view_angle_x,  self.board.view_angle_y,  self.board.view_distance,  self.board.x_pos,  self.board.y_pos,  self.board.z_pos )
#        if ( x >= 0 and x <= 23 and y >= 0 and y <= 23 ):
#            f = self.board.boardFigures[x][y]
#            if f:
#                f.damage()
#                self.redrawMyDial()
        return
    
    def moveMap(self, event):
        x,  y = self.getBoardXY(event)
        if ( x >= 0 and x <= 23 and y >= 0 and y <= 23 ):
            if self.board.moving  and ( (self.lastX == False and self.lastY == False ) or (self.lastX != x or self.lastY != y ) ) and event.x() > 0 and event.y() > 0:
                self.board.moveDestinationX = x
                self.board.moveDestinationY = y
                self.lastX = x
                self.lastY = y
                if self.board.modeObject:
                    f = self.board.boardObjects[self.board.moveOriginX][self.board.moveOriginY]
                else:
                    f = self.board.boardFigures[self.board.moveOriginX][self.board.moveOriginY]
                delta = abs( x - self.board.moveOriginX )
                dY = abs( y - self.board.moveOriginY )
                if dY > delta:
                    delta = dY
                if self.board.modeLOF:
                    self.glFrame.setTitle( "LOF "+str(delta)+" space(s)..." )
                else:
                    self.glFrame.setTitle( "Moving "+f.getName()+" "+str(delta)+" space(s)..." )
                #print self.board.moveDestinationX,  self.board.moveDestinationY
                self.board.updateGL()
        
    def stopMoving(self, event):
        if self.board.moving and not self.cmdLOF.isChecked():
            x,  y = self.getBoardXY(event)
            
            doMove = True
            if not self.board.modeObject:
                f = self.board.boardFigures[self.board.moveOriginX][self.board.moveOriginY]
                if self.board.boardFigures[self.board.moveDestinationX][self.board.moveDestinationY]:
                    doMove = False
                if f and not f.mine:
                    doMove = False
            else:
                if self.board.boardObjects[self.board.moveDestinationX][self.board.moveDestinationY]:
                    doMove = False
                f = self.board.boardObjects[self.board.moveOriginX][self.board.moveOriginY]
                    
            if doMove:
                f.x = self.board.moveDestinationX
                f.y = self.board.moveDestinationY
                if f and f.mine:
                    self.myActiveClix = (self.board.moveDestinationX, self.board.moveDestinationY)
                self.board.moveSelectedFigure()
                    
            self.glFrame.setTitle( " " )
            self.board.moving = False
            
            if self.board.modeObject:
                if not self.cmdObj.isChecked():
                    self.board.modeObject = False
            self.board.updateGL()
            
    def zoomMap(self, event):
        if (event.orientation() == QtCore.Qt.Vertical):
            #new_distance = self.board.view_distance + (float(event.delta()) / 8 / 15)
            #if ( new_distance > 0.05 and new_distance < 1 ):
            #    self.board.view_distance = new_distance
            #    self.board.updateGL()
            new_distance = self.board.z_pos + float(event.delta()) / 8
            if new_distance >= 0 and new_distance <= 40:
                self.board.z_pos = new_distance
                self.board.updateGL()
        return QtGui.QMainWindow.wheelEvent(self.MainWindow, event)
        
    def clearOtherToggles(self, button):
        if button != self.cmdBarrier:
            self.cmdBarrier.setChecked( False )
            
        if button != self.cmdSmokeCloud:
            self.cmdSmokeCloud.setChecked( False )
            
        if button != self.cmdDebris:
            self.cmdDebris.setChecked( False )
            
        if button != self.cmdSpecial:
            self.cmdSpecial.setChecked( False )
            
        if button != self.cmdLOF:
            self.cmdLOF.setChecked( False )
            self.board.modeLOF = False
            self.board.moving = False
            self.board.updateGL()
            
        if button != self.cmdObj:
            self.cmdObj.setChecked( False )
            self.board.modeObject = False
            
    @pyqtSignature("")
    def on_actionTeam_Builder_activated(self):
        self.wStack.setCurrentIndex(0)
        self.mode = "team"
    
    @pyqtSignature("")
    def on_actionBattle_Map_activated(self):
        self.wStack.setCurrentIndex(1)
        self.mode = "map"
    
    @pyqtSignature("")
    def on_txtSearch_returnPressed(self):
        #print self.txtSearch.text()
        mnm = etree.parse(os.path.join(sys.path[0], 'sets', 'mnm.xml'))
        search = str( self.txtSearch.text() )
        conditions = []
        if search is not None:
            parts = search.lower().split( " " )
            for part in parts:
                x = part.split(":")
                if len(x) == 2:
                    conditions.append( ( x[0], x[1] ) )
                    
        if len(conditions):
            for c in conditions:
                op,  val = c
                print op,  val
                
                if op == "points":
                    return
        
        
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = MainWindow()
    sys.exit(app.exec_())
