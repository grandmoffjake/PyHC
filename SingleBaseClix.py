from FigureClix import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

r = 0.5
d = 0.2
t = 2

class SingleBaseClix(FigureClix):
    def __init__(self, parent, XML):
        self.x = 0
        self.y = 0
        self.active = 0
        self.board = parent
        self.name = "Figure"
        self.mine = True
        if not XML:
            XML = """
            <figure id="mnm061" name="Dark Beast" rank="Veteran" team="The Brotherhood" range="0" targets="1" points="69"><symbols><spd>Boot</spd><atk>Fist</atk><def>Shield</def><dmg>Star</dmg></symbols><specials><atk><name>Sadistic</name><description><![CDATA[Dark Beast can use Exploit Weakness.]]></description></atk><dmg><name>Cruel Experiment</name><description><![CDATA[Give Dark Beast a power action and roll a d6. On a result of 3-6, give an action token to an adjacent opposing character with zero or one action token. On a 5 or 6, deal 2 unpreventable damage to an adjacent opposing character. On a 6, deal 1 damage to each adjacent opposing character. Apply all applicable results, which may be split among different characters.]]></description></dmg></specials><dial length="6"><click num="1"><spd power="LC">8</spd><atk power="BCF">10</atk><def power="SSE">17</def><dmg power="OUT">2</dmg></click><click num="2"><spd power="LC">8</spd><atk power="SPC">9</atk><def power="SSE">17</def><dmg power="PER">2</dmg></click><click num="3"><spd power="LC">7</spd><atk power="SPC">9</atk><def power="COM">16</def><dmg power="SPC">2</dmg></click><click num="4"><spd power="FLR">7</spd><atk>8</atk><def power="COM">16</def><dmg power="SPC">2</dmg></click><click num="5"><spd power="FLR">7</spd><atk>8</atk><def power="COM">15</def><dmg power="SPC">2</dmg></click><click num="6"><spd power="STL">9</spd><atk>7</atk><def power="SSE">17</def><dmg power="SPC">2</dmg></click></dial></figure>
            """
        
        FigureClix.__init__(self, parent, XML)
    
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
        
        glLineWidth(3);        
        glTranslatef(-0.2, 1.45,  0)
        glScalef( 0.005,  0.005,  0.005 )
        glColor(0, 0, 0)
        
        glPopMatrix()
        
        if self.tokens > 0:
            self.drawTokens()


        if self.active > 0:
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
