import math
import random

from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt4 import QtGui,  QtCore
from PyQt4.QtOpenGL import *
from Ui_mainForm import *
from GameBoard import *
from ObjectSimpleSquare import *

#TODO: Textures for terrain tokens
#TODO: Standies images/current click (interesting texture problem)
#TODO: Remove object/figure button
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
#TODO: Load teams from XML
#TODO: Fix transparency on images
#TODO: HTML dial code to XML dial code converter

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
        
        ui.cmdBarrier.mousePressEvent = self.barrier
        ui.cmdSmokeCloud.mousePressEvent = self.smokeCloud
        ui.cmdDebris.mousePressEvent = self.debris
        ui.cmdSpecial.mousePressEvent = self.special
        
        ui.cmdLOF.mousePressEvent = self.changeLOF
        ui.cmdObj.mousePressEvent = self.changeObjectMode
        
        self.myActiveClix = False
        self.theirActiveClix = False
        
        self.activeObject = False
        
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
        
    def changeLOF(self, event):
        if not self.ui.cmdLOF.isChecked():
            self.board.modeLOF = True
            self.clearOtherToggles( self.ui.cmdLOF )
        else:
            self.board.modeLOF = False
            self.ui.glFrame.setTitle( " " )
            self.board.moving = False
            self.board.updateGL()
        return QtGui.QPushButton.mousePressEvent(self.ui.cmdLOF, event)
    
    def changeObjectMode(self, event):
        if not self.ui.cmdObj.isChecked():
            self.board.modeObject = True
            self.clearOtherToggles( self.ui.cmdObj )
        else:
            self.board.modeObject = False
            self.ui.glFrame.setTitle( " " )
            self.board.moving = False
            self.board.updateGL()
        return QtGui.QPushButton.mousePressEvent(self.ui.cmdObj, event)
        
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
            if f:
                t = f.getToolTip(event.pos())
                if t:
                    QtGui.QToolTip.showText( event.globalPos(),  "<p>"+t+"</p>",  self.ui.myDial )
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
            elif (self.ui.cmdBarrier.isChecked() or self.ui.cmdSmokeCloud.isChecked() or self.ui.cmdDebris.isChecked() or self.ui.cmdSpecial.isChecked()) and not self.board.boardObjects[x][y]:
                if self.ui.cmdBarrier.isChecked():
                    type = "barrier"
                elif self.ui.cmdSmokeCloud.isChecked():
                    type = "smoke cloud"
                elif self.ui.cmdDebris.isChecked():
                    type = "debris"
                elif self.ui.cmdSpecial.isChecked():
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
                elif self.ui.cmdLOF.isChecked():
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
                    self.ui.glFrame.setTitle( "LOF "+str(delta)+" space(s)..." )
                else:
                    self.ui.glFrame.setTitle( "Moving "+f.getName()+" "+str(delta)+" space(s)..." )
                #print self.board.moveDestinationX,  self.board.moveDestinationY
                self.board.updateGL()
        
    def stopMoving(self, event):
        if self.board.moving and not self.ui.cmdLOF.isChecked():
            x,  y = self.getBoardXY(event)
            
            if not self.board.modeObject:
                f = self.board.boardFigures[self.board.moveOriginX][self.board.moveOriginY]
                if( f and f.mine ):
                    self.myActiveClix = (self.board.moveDestinationX, self.board.moveDestinationY)
            else:
                f = self.board.boardObjects[self.board.moveOriginX][self.board.moveOriginY]
                    
            f.x = self.board.moveDestinationX
            f.y = self.board.moveDestinationY
                    
            self.ui.glFrame.setTitle( " " )
            self.board.moving = False
            self.board.moveSelectedFigure()
            
            if self.board.modeObject:
                if not self.ui.cmdObj.isChecked():
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
        
    def test(self,event):
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
            
    def barrier(self, event):
        if not self.ui.cmdBarrier.isChecked():
            self.clearOtherToggles( self.ui.cmdBarrier )
            self.ui.glFrame.setTitle( "Click a square with no figure in it to add a barrier token" )
        else:
            self.ui.glFrame.setTitle( " " )
        return QtGui.QPushButton.mousePressEvent(self.ui.cmdBarrier, event)
    
    def smokeCloud(self, event):
        if not self.ui.cmdSmokeCloud.isChecked():
            self.clearOtherToggles( self.ui.cmdSmokeCloud )
            self.ui.glFrame.setTitle( "Click a square with no figure in it to add a smoke cloud token" )
        else:
            self.ui.glFrame.setTitle( " " )
        return QtGui.QPushButton.mousePressEvent(self.ui.cmdSmokeCloud, event)
            
    def debris(self, event):
        if not self.ui.cmdDebris.isChecked():
            self.clearOtherToggles( self.ui.cmdDebris )
            self.ui.glFrame.setTitle( "Click a square with no figure in it to add a debris token" )
        else:
            self.ui.glFrame.setTitle( " " )
        return QtGui.QPushButton.mousePressEvent(self.ui.cmdDebris, event)
    
    def special(self, event):
        if not self.ui.cmdSpecial.isChecked():
            self.clearOtherToggles( self.ui.cmdSpecial )
            self.ui.glFrame.setTitle( "Click a square with no figure in it to add a special token" )
        else:
            self.ui.glFrame.setTitle( " " )
        return QtGui.QPushButton.mousePressEvent(self.ui.cmdSpecial, event)
                    
        #print self.board.x_pos,  self.board.y_pos,  self.board.z_pos,  self.board.view_angle_x,  self.board.view_angle_y,  self.board.view_distance
        
    def clearOtherToggles(self, button):
        if button != self.ui.cmdBarrier:
            self.ui.cmdBarrier.setChecked( False )
            
        if button != self.ui.cmdSmokeCloud:
            self.ui.cmdSmokeCloud.setChecked( False )
            
        if button != self.ui.cmdDebris:
            self.ui.cmdDebris.setChecked( False )
            
        if button != self.ui.cmdSpecial:
            self.ui.cmdSpecial.setChecked( False )
            
        if button != self.ui.cmdLOF:
            self.ui.cmdLOF.setChecked( False )
            self.board.modeLOF = False
            self.board.moving = False
            self.board.updateGL()
            
        if button != self.ui.cmdObj:
            self.ui.cmdObj.setChecked( False )
            self.board.modeObject = False
            
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    p = PyHC(ui, MainWindow)
    sys.exit(app.exec_())
