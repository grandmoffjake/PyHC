from Clix import *
from OpenGL.GL import *
from OpenGL.GLU import *
import Image
import ImageDraw


r = 0.5
d = 0.2
t = 2

class FigureClix(Clix):
    def __init__(self, parent, XML):
        Clix.__init__(self, parent, XML)
        self.dial = self.xmlDial.find("dial")
        self.symbols = self.xmlDial.find("symbols")
        self.specials = self.xmlDial.find("specials")
        self.traits = self.xmlDial.find("traits")
        self.teams = self.xmlDial.find("teams")
        self.keywords = self.xmlDial.find("keywords")
        
        self.currentSpdPower = False
        self.currentAtkPower = False
        self.currentDefPower = False
        self.currentDmgPower = False
        self.mine = True
        self.heldObjects = []
        
        self.trait_symbol_image = self.spd_symbol_image = self.atk_symbol_image = self.def_symbol_image = self.dmg_symbol_image = False
        
        self.usePAC = True
        
        self.tokenColor = "red"
        self.tokens = 0
        
        self.target_image = Image.open( os.path.join(sys.path[0], 'images', 'units-targets-1.gif') ).convert('RGB').convert('P', palette=Image.ADAPTIVE)
        
        if self.teams:
            teams = self.teams.getchildren()
            for t in teams:
                self.team_symbols.append(Image.open( os.path.join(sys.path[0], 'images', self.getTeamImage(t.text)) ))
                
        if self.symbols is not None:
            s = self.symbols.findtext("spd")
            if s == "Wing":
                self.spd_symbol_image = Image.open( os.path.join(sys.path[0], 'images', 'units-m-wing.gif') ).convert('RGB').convert('P', palette=Image.ADAPTIVE)
            elif s == "Swim":
                self.spd_symbol_image = Image.open( os.path.join(sys.path[0], 'images', 'units-m-dolphin.gif') ).convert('RGB').convert('P', palette=Image.ADAPTIVE)
            elif s == "Transporter Boot":
                self.spd_symbol_image = Image.open( os.path.join(sys.path[0], 'images', 'units-m-transport-boot.gif') ).convert('RGB').convert('P', palette=Image.ADAPTIVE)
            elif s == "Transporter Wing":
                self.spd_symbol_image = Image.open( os.path.join(sys.path[0], 'images', 'units-m-transport-wing.gif') ).convert('RGB').convert('P', palette=Image.ADAPTIVE)
            elif s == "Transporter Swim":
                self.spd_symbol_image = Image.open( os.path.join(sys.path[0], 'images', 'units-m-transport-dolphin.gif') ).convert('RGB').convert('P', palette=Image.ADAPTIVE)
            else:
                self.spd_symbol_image = Image.open( os.path.join(sys.path[0], 'images', 'units-m-normal.gif') ).convert('RGB').convert('P', palette=Image.ADAPTIVE)

            a = self.symbols.findtext("atk")
            if a == "Duo":
                self.atk_symbol_image = Image.open( os.path.join(sys.path[0], 'images', 'units-a-duo.gif') ).convert('RGB').convert('P', palette=Image.ADAPTIVE)
            elif a == "Sharpshooter":
                self.atk_symbol_image = Image.open( os.path.join(sys.path[0], 'images', 'units-a-sharpshooter.gif') ).convert('RGB').convert('P', palette=Image.ADAPTIVE)
            else:
                self.atk_symbol_image = Image.open( os.path.join(sys.path[0], 'images', 'units-a-normal.gif') ).convert('RGB').convert('P', palette=Image.ADAPTIVE)
                
            d = self.symbols.findtext("def")
            if d == "Indomitable":
                self.def_symbol_image = Image.open( os.path.join(sys.path[0], 'images', 'units-d-indomitable.gif') ).convert('RGB').convert('P', palette=Image.ADAPTIVE)
            else:
                self.def_symbol_image = Image.open( os.path.join(sys.path[0], 'images', 'units-d-normal.gif') ).convert('RGB').convert('P', palette=Image.ADAPTIVE)
                
            g = self.symbols.findtext("dmg")
            if g == "Colossal":
                self.dmg_symbol_image = Image.open( os.path.join(sys.path[0], 'images', 'units-g-fist.gif') ).convert('RGB').convert('P', palette=Image.ADAPTIVE)
            elif g == "Giant":
                self.dmg_symbol_image = Image.open( os.path.join(sys.path[0], 'images', 'units-g-giant.gif') ).convert('RGB').convert('P', palette=Image.ADAPTIVE)
            else:
                self.dmg_symbol_image = Image.open( os.path.join(sys.path[0], 'images', 'units-g-normal.gif') ).convert('RGB').convert('P', palette=Image.ADAPTIVE)
            
        if self.traits:
            self.trait_symbol_image = Image.open( os.path.join(sys.path[0], 'images', 'trait-star.gif') ).convert('RGB').convert('P', palette=Image.ADAPTIVE)
            
    def getTeamImage(self, team):
        if team == "X-Men":
            return "units-ta-xmen-a.gif"
        else:
            return "units-ta-supermanenemy.png"
        
    def describeFeats(self):
        return ""
            
    def describeKeywords(self):
        if self.keywords:
            k = []
            for keyword in self.keywords.getchildren():
                k.append( keyword.text )
            return ", ".join( k )
        return ""
        
    def describeTeamAbilities(self):
        return "<b>"+"X-Men"+"</b><br/>Buncha text"
        
    def describeTraits(self):
        if self.traits:
            t = self.traits.getchildren()
            s = ""
            for trait in t:
                if s:
                    s += "<br/>"
                s += "<b>"+trait.get("name")+"</b><br/>"+trait.get("description") 
                
            return s
        return ""
        
    def describeAbility(self, position):
        t = self.symbols.findtext(position)
        if t:
            return self.board.PAC.getAbilityDescription(t)
        return position
            
    def describePower(self, position, code):
        if code == "SPC":
            c = self.specials.find(position)
            if c:
                return "<b>"+c.findtext("name") + "</b><br/>" + c.findtext("description")
        elif code:
            return self.board.PAC.getDescription(code)
        
        return ""
        
    def token(self, color):
        if color == "blue":
            self.tokenColor = "blue"
        else:
            self.tokenColor = "red"
            
        if self.tokens < 2:
            self.tokens += 1
            self.board.log( "Me",  self.getName() + " added a " + color + " action token." )
        else:
            self.tokens = 0
            self.board.log( "Me",  self.getName() + " cleared." )
            
    def takeObject(self,  o):
        o.heldBy = self
        self.heldObjects.append( o )
        self.board.boardObjects[o.x][o.y] = False
        self.board.log( "Me",  self.getName() + " picked up " + o.getName() + "." )
        return True
        
    def dropObject(self):
        if len(self.heldObjects)>0:
            square = False
            if not self.board.boardObjects[self.x][self.y]:
                square = (self.x, self.y)
            else:
                for i in range(self.x-1, self.x+1):
                    for j in range(self.y-1, self.y+1):
                        if not self.board.boardObjects[i][j]:
                            square = (i, j)
                            break
                            
            if square:
                o = self.heldObjects.pop()
                o.x = square[0]
                o.y = square[1]
                self.board.boardObjects[o.x][o.y] = o
                o.heldBy = False
                self.board.log( "Me",  self.getName() + " dropped " + o.getName() + "." )
            else:
                self.board.log( "Me",  self.getName() + " cannot drop object." )
                
    def hasObject(self):
        if len(self.heldObjects) > 0:
            return True
        return False
        
    def regenerateTexture(self):
        if self.texture:
            #im = Image.open(os.path.join(sys.path[0], 'assets', 'barrier.png'))
            #BarrierData = im.convert("RGBA").tostring("raw", "RGBA")
            im = Image.new('RGBA', (100, 150))
            draw = ImageDraw.Draw(im)
            #draw.ellipse( (0, 0, 150, 150 ),  fill="black" )
            im, draw = self.drawTexture(im, draw)
            TextureData = im.convert("RGBA").tostring("raw", "RGBA")

            glBindTexture(GL_TEXTURE_2D, self.texture)
            glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, im.size[0], im.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, TextureData )
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            self.board.updateGL()

            
    def draw(self):
        glPushMatrix()
        
        h = 12
        glDisable(GL_TEXTURE_2D)
        glRotatef(90,  1.0, 0.0, 0.0)
        glTranslatef(-h+r+self.x, -h+r+self.y,  -d)
        
        glPushMatrix()
        
        if self.active == 1:
            cR = 0.1
            cG = 0.8
            cB = 0.1
        elif self.active == 2:
            cR = 0.1
            cG = 1
            cB = 1
        else:
            cR = 0.1
            cG = 0.1
            cB = 0.1
        glColor(cR, cG, cB)
        self.drawBase()
        
        glRotatef(-90,  1.0, 0.0, 0.0)
        
        glRotatef(-self.board.view_angle_y, 0.0, 1.0, 0.0)
        glColor(1, 1, 1)
        if self.texture:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture)
            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 1.0); glVertex3f(-r, 0, 0.0)
            glTexCoord2f(1.0, 1.0); glVertex3f(r, 0, 0.0)
            glTexCoord2f(1.0, 0.0); glVertex3f(r, t, 0.0)
            glTexCoord2f(0.0, 0.0); glVertex3f(-r, t, 0.0)
            glEnd()
            glDisable(GL_TEXTURE_2D)
        else:
            glRectf( -r,  0,  r,  t )
        
        glPopMatrix()
        
        if self.tokens > 0:
            self.drawTokens()
            
        if self.hasObject():
            self.drawObjects()
            
        glPopMatrix()
        return

        if self.active > 0:
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
            glEnable(GL_BLEND);
            if self.active == 1:
                cR = 0.1
                cG = 1
                cB = 0.1
            elif self.active == 2:
                cR = 0.1
                cG = 1
                cB = 1
            glScalef(1.2, 1.2, 1.2)
            glColor4f(cR, cG, cB, .5)
            self.drawBase()
            glScalef(1.25, 1.25, 1.25)
            glColor4f(cR, cG, cB, .2)
            self.drawBase()
            
    def drawObjects(self):
        glPushMatrix()
        #glRotatef(-self.board.view_angle_y, 0.0, 1.0, 0.0)
        
        glTranslatef( 0.2,  0,  0 )
        for o in self.heldObjects:
            glTranslatef( 0.1,  0,  -0.1 )
            o.draw()

        
        glPopMatrix()
            
    def drawValues(self, im, draw, click, font, xOffset):
        x = 65+xOffset
        y = 68
        dY = 24
        dX = 13
        
        spd_text = atk_text = def_text = dmg_text = "black"
        
        if click:
            self.currentSpdPower = click[0].get("power")
            self.currentAtkPower = click[1].get("power")
            self.currentDefPower = click[2].get("power")
            self.currentDmgPower = click[3].get("power")
            
            spd_box = [(60+xOffset, 67), (78+xOffset, 85)]
            atk_box = [(60+xOffset, 90), (78+xOffset, 108)]
            def_box = [(60+xOffset, 115), (78+xOffset, 133)]
            dmg_box = [(83+xOffset, 114), (101+xOffset, 132)]

            if self.currentSpdPower == "SPC":
                draw.rectangle( spd_box,  outline="black",  fill="white" )
            elif self.currentSpdPower:
                c = self.board.PAC.getColors(self.currentSpdPower)
                spd_text = c[1]
                draw.rectangle( spd_box,  fill=c[0] )
        
            if self.currentAtkPower == "SPC":
                draw.rectangle( atk_box,  outline="black",  fill="white" )
            elif self.currentAtkPower:
                c = self.board.PAC.getColors(self.currentAtkPower)
                atk_text = c[1]
                draw.rectangle( atk_box,  fill=c[0] )
        
            if self.currentDefPower == "SPC":
                draw.rectangle( def_box,  outline="black",  fill="white" )
            elif self.currentDefPower:
                c = self.board.PAC.getColors(self.currentDefPower)
                def_text = c[1]
                draw.rectangle( def_box,  fill=c[0] )
        
            if self.currentDmgPower == "SPC":
                draw.rectangle( dmg_box,  outline="black",  fill="white" )
            elif self.currentDmgPower:
                c = self.board.PAC.getColors(self.currentDmgPower)
                dmg_text = c[1]
                draw.rectangle( dmg_box,  fill=c[0] )
        
        offset = 0
        if len(click[0].text) > 1:
            offset = 4
        spd_xy = (x-offset, y)
        
        offset = 0
        if len(click[1].text) > 1:
            offset = 4
        atk_xy = (x-offset,  y+dY)
        
        offset = 0
        if len(click[2].text) > 1:
            offset = 4
        def_xy = (x-offset,  y+dY+dY)
        
        offset = 0
        if len(click[3].text) > 1:
            offset = 4
        dmg_xy = (x+24-offset,  y+dY+dY-1)
        
        draw.text( spd_xy,  click[0].text,  font=font,  fill=spd_text )
        draw.text( atk_xy,  click[1].text,  font=font,  fill=atk_text )
        draw.text( def_xy,  click[2].text,  font=font,  fill=def_text )
        draw.text( dmg_xy,  click[3].text,  font=font,  fill=dmg_text )
        
        return draw
