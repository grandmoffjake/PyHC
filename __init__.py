import math
import random

from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt4 import QtGui,  QtCore
from PyQt4.QtOpenGL import *
from Ui_mainForm import *
from GameBoard import *

class PyHC(Ui_MainWindow):
    ''' Example class for using SpiralWidget'''
    
    def __init__(self, ui, MainWindow):
        self.mousePosition = [0, 0]
        self.MainWindow = MainWindow
        self.ui = ui
        ui.glFrame.setTitle( " " )
        self.board = GameBoard(MainWindow, ui)
        ui.vLayout.addWidget(self.board)
        ui.gameLog.keyPressEvent = self.test
        MainWindow.keyPressEvent = self.test
        self.board.wheelEvent = self.zoomMap
        self.board.mouseMoveEvent = self.moveMap
        self.board.mouseDoubleClickEvent = self.doubleClickMap
        self.board.mousePressEvent = self.clickMap
        self.board.mouseReleaseEvent = self.stopMoving
        self.lastX = False
        self.lastY = False
        
        ui.cmdHeal.mousePressEvent = self.healClix
        ui.cmdDamage.mousePressEvent = self.damageClix
        ui.cmdTokenRed.mousePressEvent = self.tokenRed
        ui.cmdTokenBlue.mousePressEvent = self.tokenBlue
        ui.rollOne.mousePressEvent = self.rollOne
        ui.rollTwo.mousePressEvent = self.rollTwo
        
        self.myActiveClix = False
        self.theirActiveClix = False
        
        ui.myDial.setMouseTracking(True)
        ui.myDial.mouseMoveEvent = self.hoverMyDial
        
    def getMyActiveClix(self):
        c = self.myActiveClix
        if c:
            x,  y = c
            f = self.board.boardFigures[x][y]
            if f:
                return f
                
        return False
        
    def rollOne(self, event):
        v = random.randint( 1,  6 )
        self.board.log( "Me",  "Rolled a "+str(v)+" on one die.")
        return QtGui.QPushButton.mousePressEvent(self.ui.rollOne, event)
    
    def rollTwo(self, event):
        v = random.randint( 2,  12 )
        s = "Rolled a "+str(v)+" on two dice."
        if v == 2:
            s += "  <b>Crit miss!</b>"
        elif v == 12:
            s += "  <b>Critical hit!</b>"
        self.board.log( "Me",  s )
        return QtGui.QPushButton.mousePressEvent(self.ui.rollTwo, event)
        
    def healClix(self, event):
        f = self.getMyActiveClix()
        if f:
            f.heal()
            self.redrawMyDial()
            
        return QtGui.QPushButton.mousePressEvent(self.ui.cmdHeal, event)
    
    def damageClix(self, event):
        f = self.getMyActiveClix()
        if f:
            f.damage()
            self.redrawMyDial()
            
        return QtGui.QPushButton.mousePressEvent(self.ui.cmdDamage, event)
        
    def tokenRed(self, event):
        f = self.getMyActiveClix()
        if f:
            f.token( "red" )
            self.board.updateGL()
            
        return QtGui.QPushButton.mousePressEvent(self.ui.cmdTokenRed, event)
        
    def tokenBlue(self, event):
        f = self.getMyActiveClix()
        if f:
            f.token( "blue" )
            self.board.updateGL()

        return QtGui.QPushButton.mousePressEvent(self.ui.cmdTokenBlue, event)
    
        
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
            t = f.getToolTip(event.pos())
            if t:
                QtGui.QToolTip.showText( event.globalPos(),  "<p>"+t+"</p>",  self.ui.myDial )
            else:
                QtGui.QToolTip.hideText()
        
    def clickMap(self, event):
        x,  y = self.getBoardXY(event)
        if ( x >= 0 and x <= 23 and y >= 0 and y <= 23 ):
            if ( self.board.boardFigures[x][y] ):
                f = self.board.boardFigures[x][y]
                self.board.moving = True
                self.board.moveOriginX = self.board.moveDestinationX = x
                self.board.moveOriginY = self.board.moveDestinationY = y
                
                #self.board.clearMyActive()
                if f.mine:
                    self.myActiveClix = (x, y)
                    f.active = 1
                    self.redrawMyDial()
                else:
                    self.theirActiveClix = (x, y)
                    f.active = 2
                    self.redrawTheirDial()
            
    def redrawMyDial(self):
        f = self.board.boardFigures[self.myActiveClix[0]][self.myActiveClix[1]]
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(f.drawDial(), "PNG")
        ui.myDial.setPixmap( pixmap )
        ui.myDial.update()
        
    def redrawTheirDial(self):
        f = self.board.boardFigures[self.theirActiveClix[0]][self.theirActiveClix[1]]
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(f.drawDial(), "PNG")
        ui.theirDial.setPixmap( pixmap )
        ui.theirDial.update()
        
    def doubleClickMap(self, event):
        x, y = self.getBoardXY(event)
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
                f = self.board.boardFigures[self.board.moveOriginX][self.board.moveOriginY]
                delta = abs( x - self.board.moveOriginX )
                dY = abs( y - self.board.moveOriginY )
                if dY > delta:
                    delta = dY
                self.ui.glFrame.setTitle( "Moving "+f.getName()+" "+str(delta)+" space(s)..." )
                #print self.board.moveDestinationX,  self.board.moveDestinationY
                self.board.updateGL()
        
    def stopMoving(self, event):
        if self.board.moving:
            if( self.myActiveClix ):
                self.myActiveClix = (self.board.moveDestinationX, self.board.moveDestinationY)
            self.ui.glFrame.setTitle( " " )
            self.board.moving = False
            self.board.moveSelectedFigure()
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
        
    def test(self,event):
        print event.key()
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
            
        #print self.board.x_pos,  self.board.y_pos,  self.board.z_pos,  self.board.view_angle_x,  self.board.view_angle_y,  self.board.view_distance
        
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    p = PyHC(ui, MainWindow)
    sys.exit(app.exec_())
