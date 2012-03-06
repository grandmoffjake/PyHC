'''
GameBoard - got my starting point from Stou Sandalski's SpiralWidget demo:
http://www.siafoo.net/snippet/316

Got the board starting point from Ian Mallett's Pente implementation
http://www.geometrian.com/Programs.php
'''

import math
import Image
from fractions import Fraction
from SingleBaseClix import *
from MapLine import *

from OpenGL.GL import *
from OpenGL.GLU import *

from PyQt4 import QtGui
from PyQt4.QtOpenGL import *
from PAC import *

class GameBoard(QGLWidget):
    
    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.view_angle_x = 90
        self.view_angle_y = 0
        self.view_distance = 1.0
        self.x_pos = 0.0
        self.y_pos = 0.0
        self.z_pos = 0.0
        self.PAC = PAC()
        
        self.moving = False
        self.moveOriginX = 0
        self.moveOriginY = 0
        self.moveDestinationX = 0
        self.moveDestinationY = 0
        
        self.boardFigures = []
        for i in range(0, 24):
            self.boardFigures.append([False]*24)
        
        s = SingleBaseClix(self)
        s.x = 2
        s.y = 2
        s.name = "Batman"
        
        b = SingleBaseClix(self)
        b.x = 23
        b.y = 2
        b.active = 2
        b.name = "Wolverine"
        
        self.boardFigures[b.x][b.y] = b
        self.boardFigures[s.x][s.y] = s
        

        self.setMinimumSize(500, 500)

    def paintGL(self):
        '''
        Drawing routine
        '''
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        if (hasattr( self,  'Textures') == False):
            self.Textures = glGenTextures(2)
            
            GridFile = '/Users/thejake/Documents/HCOL/maps/Small_Town.jpg'
            im = Image.open(GridFile)
            gx = im.size[0]
            gy = im.size[1]
            GridData = im.convert("RGBA").tostring("raw", "RGBA")
            
            glEnable(GL_TEXTURE_2D)
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
            
            glBindTexture(GL_TEXTURE_2D, self.Textures[0]) #Board (Red Section)
            glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, gx, gy, 0,
                          GL_RGBA, GL_UNSIGNED_BYTE, GridData )
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        
        glTranslatef(self.x_pos, self.y_pos, -30.0*self.view_distance+self.z_pos)
        glRotatef(self.view_angle_x,  1.0, 0.0, 0.0)
        glRotatef(self.view_angle_y, 0.0, 1.0, 0.0)

        w = 0.99
        h = 12.0
        s = 2.0
        
        glDisable(GL_TEXTURE_2D)
        glColor(0.3, 0.3, 0.3)
        glBegin(GL_QUADS)
        glVertex3f(-h, 0.0, h)
        glVertex3f(h, 0.0, h)
        glVertex3f(h, -s, h)
        glVertex3f(-h, -s, h)
        
        glVertex3f(-h, -s, h)
        glVertex3f(-h, -s, -h)
        glVertex3f(-h, 0.0, -h)
        glVertex3f(-h, 0.0, h)
        
        glVertex3f(-h, 0.0, -h)
        glVertex3f(h, 0.0, -h)
        glVertex3f(h, -s, -h)
        glVertex3f(-h, -s, -h)
        
        glVertex3f(h, 0.0, -h)
        glVertex3f(h, 0.0, h)
        glVertex3f(h, -s,  h)
        glVertex3f(h, -s, -h)
        
        glEnd();
        
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.Textures[0]) #Board (Red Section)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); glVertex3f(-h, 0.0, -h)
        glTexCoord2f(1.0, 0.0); glVertex3f(h, 0.0, -h)
        glTexCoord2f(1.0, 1.0); glVertex3f(h, 0.0, h)
        glTexCoord2f(0.0, 1.0); glVertex3f(-h, 0.0, h)
        glEnd();

        for i in range(0, 24):
            for j in range(0, 24):
                if self.boardFigures[i][j]:
                    self.boardFigures[i][j].draw()
                    
        if self.moving:
            self.drawMoveLine()
        
        #glEnableClientState(GL_VERTEX_ARRAY)
        
        glFlush()

    def resizeGL(self, w, h):
        '''
        Resize the GL window 
        '''
        
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 1.0*w/h, 0.5, 1000.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    
    def initializeGL(self):
        '''
        Initialize GL
        '''
        
        # set viewing projection
        glEnable(GL_BLEND)                                          #masking functions
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
            
        glShadeModel(GL_SMOOTH)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable( GL_ALPHA_TEST )
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        
    def s(self, x, y):
        return [round(x/2.10176)*2.10176,  round(y/2.10176)*2.10176]
    def viewport(self):
        return glGetIntegerv(GL_VIEWPORT)
    def modelview(self):
        return glGetDoublev(GL_MODELVIEW_MATRIX)
    def projection(self):
        return glGetDoublev(GL_PROJECTION_MATRIX)
    def getMouseZ(self,  x,  y):
        return glReadPixels(x, y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
        
    def drawMoveLine(self):
        glPushMatrix()
        glColor(0, 0,  0)
        #glRotatef(15,  0.0, 1.0, 0.0)
        glTranslatef(0, 0.2, 0)
        h = 4
        glBegin(GL_QUADS)
        #glRectf( self.moveOriginX-11,  self.moveOriginY-11,  self.moveDestinationX-11,  self.moveDestinationY-11 )
        x1 = self.moveOriginX-11.5
        y1 = self.moveOriginY-11.5
        x2 = self.moveDestinationX-11.5
        y2 = self.moveDestinationY-11.5
        
        if y2-y1 !=0:
            slope = (x2-x1)/(y2-y1)
            #print slope
        
        glVertex3f(x1-.1, 0.0, y1-.1)
        glVertex3f(x1+.1, 0.0, y1+.1)
        glVertex3f(x2+.1, 0.0, y2+.1)
        glVertex3f(x2-.1, 0.0, y2-.1)
        glEnd()
        #print self.moveOriginX,  self.moveOriginY,  self.moveDestinationX,  self.moveDestinationY
        glPopMatrix()
        
        self.highlightSquare( self.moveDestinationX,  self.moveDestinationY )
        
        #Just testing this - it needs to move to the Line of Fire mode instead
        dX = self.moveDestinationX-self.moveOriginX
        dY = self.moveDestinationY-self.moveOriginY
        
        if ( abs(dX) > 1 and abs(dY) >1 ):
            l = self.findPath( int(self.moveOriginX),  int(self.moveOriginY),  int(self.moveDestinationX), int(self.moveDestinationY) )
            for coord in l:
                x,  y = coord
                if ( x != self.moveOriginX and y != self.moveOriginY ) and ( x != self.moveDestinationX and y != self.moveDestinationY ):
                    self.highlightSquare( x,  y )

        
    def highlightSquare(self, x,  y):
        glPushMatrix()
        glRotatef(90,  1.0, 0.0, 0.0)
        glTranslatef(0, 0, -0.1)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        glEnable(GL_BLEND);
        glColor4f(.1, 1, .1, 0.2)
        glRectf( x-12,  y-12,  x-11,  y-11 )
        glPopMatrix()
        return
        
    def clearMyActive(self):
        for i in range(0, 24):
            for j in range(0, 24):
                if self.boardFigures[i][j] and self.boardFigures[i][j].active == 1:
                    self.boardFigures[i][j].active = 0
                    
    def moveSelectedFigure(self):
        if self.moveOriginX != self.moveDestinationX or self.moveOriginY != self.moveDestinationY:
            if self.boardFigures[self.moveOriginX][self.moveOriginY] and self.boardFigures[self.moveOriginX][self.moveOriginY].mine and self.boardFigures[self.moveDestinationX][self.moveDestinationY] == False:
                self.boardFigures[self.moveOriginX][self.moveOriginY].x = self.moveDestinationX
                self.boardFigures[self.moveOriginX][self.moveOriginY].y = self.moveDestinationY
                self.boardFigures[self.moveDestinationX][self.moveDestinationY] = self.boardFigures[self.moveOriginX][self.moveOriginY]
                self.boardFigures[self.moveOriginX][self.moveOriginY] = False
                    
    '''
    findPath designed by Dr. Brandon Humpert - thanks for the help!
    '''
    def findPath(self, x1, y1, x2, y2):
        ''' Given coords (x1, y1) and (x2, y2) for the centers of
        squares in a square grid, find_path returns a list of tuples of square's
        coords, whose interiors are intersected by the line from (x1, y1) to
        (x2, y2) '''
        dx = int(x2 - x1)
        dy = int(y2 - y1)
        xdir = int(copysign(1, dx))
        ydir = int(copysign(1, dy))
        dx = int(abs(dx))
        dy = int(abs(dy))
        L = MapLine(x1, y1, x2, y2)

        # For every place that the line intersects the grid, we will add the
        # *next* square on the path, so we initialize with the first square.
        pathsquares = [(x1, y1)]

        # Generate a list of parameters corresponding to line/grid intersections
        params = [Fraction(2 * i + 1, 2 * dx) for i in range(dx)]
        params.extend([Fraction(2 * i + 1, 2 * dy) for i in range(dy)])

        # Throw out duplicate values and (for readability) sort the list
        params = list(set(params))
        params = sorted(params)

        for param in params:
            x, y = L.getpoint(param)
            if x.denominator == 2:
                # if intersecting a vertical grid line
                if y.denominator == 2:
                    # if *also* intersecting a horizontal grid line
                    pathsquares.append((int(x + Fraction(1, 2) * xdir),
                                        int(y + Fraction(1, 2) * ydir)))
                    continue
                else:
                    # only intersecting vertical
                    pathsquares.append((int(x + Fraction(1, 2) * xdir),
                                        int(floor(y + Fraction(1, 2)))))
                    continue
            else:
                # only intersecting horizontal
                pathsquares.append((int(floor(x + Fraction(1, 2))),
                                    int(y + Fraction(1, 2) * ydir)))

        return pathsquares
