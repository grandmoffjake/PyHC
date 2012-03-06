import math

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
        self.board = GameBoard(MainWindow)
        ui.vLayout.addWidget(self.board)
        MainWindow.keyPressEvent = self.test
        self.board.wheelEvent = self.zoomMap
        self.board.mouseMoveEvent = self.moveMap
        self.board.mouseDoubleClickEvent = self.doubleClickMap
        self.board.mousePressEvent = self.clickMap
        self.board.mouseReleaseEvent = self.stopMoving
        self.lastX = False
        self.lastY = False
        
    def getBoardXY(self, event):
        v = self.board.viewport()
        winY = v[3] - event.y()
        winX = event.x()
        #print event.x(),  event.y(),  winX,  winY
        #if ( winX > 0 and winY > 0 ):
        winZ = self.board.getMouseZ(winX, winY)
        posX, posY, posZ = gluUnProject(winX, winY, winZ)
        #self.board.x_pos = posX*-1
        #m = 90-self.board.view_angle_x
        #self.board.z_pos = posZ*m
        #self.board.updateGL()
        
        #print math.ceil(posX)+11,  math.ceil(posZ)+11,  posX,  posZ
        x = int(math.ceil(posX)+11)
        y = int(math.ceil(posZ)+11)
        
        return [x, y]
        #else:
        #    return [0, 0]
        
    def clickMap(self, event):
        x,  y = self.getBoardXY(event)
        if ( self.board.boardFigures[x][y] and self.board.boardFigures[x][y].mine ):
            self.board.moving = True
            self.board.moveOriginX = self.board.moveDestinationX = x
            self.board.moveOriginY = self.board.moveDestinationY = y
        #print self.board.moveOriginX,  self.board.moveOriginY
        
    def doubleClickMap(self, event):
        x, y = self.getBoardXY(event)
        f = self.board.boardFigures[x][y]
        if ( f ):
            self.board.clearMyActive()
            if f.mine:
                f.active = 1
            else:
                f.active = 2
                
            print f.name
            #print f.drawDial()
            print f.getClick()
            print f.describePower("spd", "SPC")
            #qimg = QtGui.QImage.fromData(f.drawDial())
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(f.drawDial(), "PNG")
            #ui.myDial.setText( f.getName() )
            ui.myDial.setPixmap( pixmap )
            ui.myDial.update()
            #ui.dialsLayout.addWidget(qimg)
            self.board.updateGL()
        
    def moveMap(self, event):
        x,  y = self.getBoardXY(event)
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
