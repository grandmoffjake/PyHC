from Clix import *
from OpenGL.GL import *
from OpenGL.GLU import *
import Image
import ImageDraw
import ImageFont
import StringIO
import os
import sys

r = 0.65
d = 0.1
t = 2

class ObjectSimpleClix(Clix):
    def __init__(self, parent, XML):
        Clix.__init__(self, parent, XML)
        
        self.baseColor = "red"
        t = self.xmlDial.get("type")
        
        self.x = 0
        self.y = 0
        self.active = 0
        self.mine = True
        self.heldBy = False
        
        if t == "heavy":
            self.baseColor = "red"
        elif t == "light":
            self.baseColor = "yellow"
        elif t == "immobile" or t == "relic":
            self.baseColor = "blue"
        
    def getName(self):
        return self.xmlDial.get("name")
        
    def getId(self):
        return self.xmlDial.get("id")
        
    def getPoints(self):
        return self.xmlDial.get("points")
        
    def canBePickedUp(self):
        return True
            
    def draw(self):
        glPushMatrix()
        
        h = 12
        glDisable(GL_TEXTURE_2D)
        if not self.heldBy:
            glRotatef(90,  1.0, 0.0, 0.0)
            glTranslatef(-h+0.5+self.x, -h+0.5+self.y,  -d)
        
        self.drawBase()
        
        glPopMatrix()
        
    def drawBase(self):
        if self.baseColor == "red":
            glColor( 0.8, 0, 0 )
        elif self.baseColor == "yellow":
            glColor( 1, 1, 0 )
        elif self.baseColor == "blue":
            glColor( 0, 0,  0.8 )
        q = gluNewQuadric()
        gluQuadricNormals(q, GLU_SMOOTH)
        gluQuadricOrientation( q, GLU_INSIDE );
        gluDisk( q, 0.0, r, 10, 10)
        
    def drawDial(self):
        im = Image.new('RGBA', (150, 150),  (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        draw.ellipse( (0, 0, 150, 150 ),  fill=self.baseColor )
        
        fontPath = "/Library/Fonts/"
        font = ImageFont.truetype(fontPath+"Arial.ttf", 14)
        clickNumFont = ImageFont.truetype(fontPath+"Arial.ttf", 10)
        dialTopFont = ImageFont.truetype(fontPath+"Arial.ttf", 12)
        
        draw.text( (11,  45),  self.getName(),  font=dialTopFont,  fill="black" )
        draw.text( (15,  33),  self.getId(),  font=clickNumFont,  fill="black" )

        draw.text( (150-25-(3*len(str(self.getPoints()))), 33),  self.getPoints(),  font=clickNumFont,  fill="black")
            
        #This solution is ignorant, but for some reason Image.tostring can't get PNG data or any format easily understood by QPixmap
        output = StringIO.StringIO()
        im.save(output, "PNG")
        contents = output.getvalue()
        output.close()
        
        return contents
