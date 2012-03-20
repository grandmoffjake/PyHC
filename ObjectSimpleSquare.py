from OpenGL.GL import *
from OpenGL.GLU import *
import Image
import ImageDraw
import ImageFont
import StringIO
import os
import sys

r = 0.5
d = 0.1
t = 2

class ObjectSimpleSquare():
    def __init__(self, parent,  type):
        self.board = parent
        self.x = 0
        self.y = 0
        self.active = 0
        self.mine = True
        self.type = type
        
    def getName(self):
        return self.type + " token"
        
    def canBePickedUp(self):
        return False
                    
    def draw(self):
        glPushMatrix()
        
        h = 12
        glDisable(GL_TEXTURE_2D)
        glRotatef(90,  1.0, 0.0, 0.0)
        glTranslatef(-h+0.5+self.x, -h+0.5+self.y,  -d)
        
        self.drawBase()
        
        glPopMatrix()
        
    def drawBase(self):
        glEnable(GL_TEXTURE_2D)
        
        if self.type == "barrier":
        #    glColor( 0.65, 0.454, 0 )
            glBindTexture(GL_TEXTURE_2D, self.board.namedTextures['barrier'])
        elif self.type == "smoke cloud":
            glBindTexture(GL_TEXTURE_2D, self.board.namedTextures['smokecloud'])
        #    glColor( 0.498, 0.349, 0.5294 )
        elif self.type == "debris":
            glBindTexture(GL_TEXTURE_2D, self.board.namedTextures['debris'])
        #    glColor( 0.6313, 0.6313,  0.6313 )
        elif self.type == "special":
            glBindTexture(GL_TEXTURE_2D, self.board.namedTextures['special'])
        #    glColor( 0, 0,  1 )
            
        
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); 
        glVertex3f(-r, -r, 0.0)
        glTexCoord2f(1.0, 0.0); 
        glVertex3f(r, -r, 0.0)
        glTexCoord2f(1.0, 1.0); 
        glVertex3f(r, r, 0.0)
        glTexCoord2f(0.0, 1.0); 
        glVertex3f(-r, r, 0.0)
        glEnd()
            
        #glRectf( -r,  -r,  r,  r )
        
    def drawDial(self):
        return False
