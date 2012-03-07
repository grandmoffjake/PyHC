from Clix import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

r = 0.5
d = 0.2
t = 2

class SingleBaseClix(Clix):
    def __init__(self, parent):
        self.x = 0
        self.y = 0
        self.active = 0
        self.board = parent
        self.name = "Figure"
        self.mine = True
        Clix.__init__(self, parent)
    
    def draw(self):
        glPushMatrix()
        
        h = 12
        glDisable(GL_TEXTURE_2D)
        glRotatef(90,  1.0, 0.0, 0.0)
        glTranslatef(-h+r+self.x, -h+r+self.y,  -d)
        
        glPushMatrix()
        
        glColor(0.1, 0.1, 0.1)
        self.drawBase()
        
        glRotatef(-90,  1.0, 0.0, 0.0)
        
        glRotatef(-self.board.view_angle_y, 0.0, 1.0, 0.0)
        glColor(255, 255, 255)
        glRectf( -r,  0,  r,  t )
        
#        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
#        glEnable(GL_BLEND);
#        glEnable(GL_LINE_SMOOTH);
        glLineWidth(3);        
        glTranslatef(-0.2, 1.45,  0)
        glScalef( 0.005,  0.005,  0.005 )
        glColor(0, 0, 0)
        
        glPopMatrix()
        
        if self.tokens > 0:
            self.drawTokens()


        if self.active > 0:
            #glPushMatrix()
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
            glEnable(GL_BLEND);
            if self.active == 1:
                cR = 1
                cG = 0.1
                cB = 0.1
            elif self.active == 2:
                cR = 0.1
                cG = 0.1
                cB = 1
            glScalef(1.2, 1.2, 1.2)
            glColor4f(cR, cG, cB, .5)
            self.drawBase()
            glScalef(1.25, 1.25, 1.25)
            glColor4f(cR, cG, cB, .2)
            self.drawBase()
            #glPopMatrix()
                        
        glPopMatrix()
            
            
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
        gluQuadricDrawStyle( q,  GLU_FILL )
        gluCylinder( q,  r,  r,  d,  10,  10 )
        
        q = gluNewQuadric()
        gluQuadricNormals(q, GLU_SMOOTH)
        gluQuadricOrientation( q, GLU_INSIDE );
        gluDisk( q, 0.0, r, 10, 10)
