from FigureClix import *
from OpenGL.GL import *
from OpenGL.GLU import *
from lxml import etree

class SingleBaseClix(FigureClix):
    def __init__(self, parent, XML):
        self.x = 0
        self.y = 0
        self.active = 0        
        FigureClix.__init__(self, parent, XML)
            
    def drawTokens(self):
        glPushMatrix()
        glRotatef(-self.board.view_angle_y, 0.0, 1.0, 0.0)
        if self.tokenColor == "red":
            cR = 1
            cG = 0.1
            cB = 0.1
        else:
            cR = 0.1
            cG = 0.1
            cB = 1
            
        glColor(cR, cG, cB)
        
        if self.tokens == 2:
            q = gluNewQuadric()
            glTranslatef( 0.25,  0.5,  -0.25 )
            gluSphere( q,  0.15,  10,  10 )
            
            q = gluNewQuadric()
            glTranslatef( -0.5,  0,  0 )
            gluSphere( q,  0.15,  10,  10 )
        else:
            q = gluNewQuadric()
            glTranslatef( 0.25,  0.5,  -0.25 )
            gluSphere( q,  0.15,  10,  10 )
            
        glPopMatrix()

    def drawBase(self):

        q = gluNewQuadric()
        gluQuadricNormals(q, GLU_SMOOTH)
        gluQuadricOrientation( q, GLU_INSIDE );
        gluDisk( q, 0.0, r, 10, 10)

        glColor( 0.1,  0.1,  0.1 )
        q = gluNewQuadric()
        gluQuadricNormals(q, GLU_SMOOTH)
        gluQuadricDrawStyle( q,  GLU_FILL )
        gluCylinder( q,  r,  r,  d,  10,  10 )

