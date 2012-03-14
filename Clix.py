import xml.etree.ElementTree as ET
import Image
import ImageDraw
import ImageFont
import StringIO
import os
import sys

class Clix:
    def __init__(self, parent, XML):
        self.xmlDial = ET.fromstring(XML)
        self.board = parent
        self.currentClick = 1
        self.team_symbols = []
        
        self.drawWindow = True
        
        self.spd_box = [(60, 67), (78, 85)]
        self.atk_box = [(60, 90), (78, 108)]
        self.def_box = [(60, 115), (78, 133)]
        self.dmg_box = [(83, 114), (101, 132)]
        
        self.images_path = os.path.join(sys.path[0], 'images')
        
        return 
        
    def getId(self):
        return self.xmlDial.get("id")
        
    def getRange(self):
        if self.xmlDial.get("range"):
            return (self.xmlDial.get("range"), self.xmlDial.get("targets"))
        
        return False
        
    def getPoints(self):
        return self.xmlDial.get("points")
        
    def getName(self):
        return self.xmlDial.get("name")
        
    def getRank(self):
        return self.xmlDial.get("rank")
        
    def getClicks(self):
        return int(self.dial.get("length"))
        
    def heal(self):
        if self.currentClick > 1:
            self.currentClick -= 1
            self.board.log( "Me", self.getName() + " healed 1 click." )
            
    def damage(self):
        if self.currentClick < self.getClicks()+1:
            self.currentClick += 1
            self.board.log( "Me", self.getName() + " was damaged 1 click." )
            
    def getClick(self):
        if self.getClicks()<self.currentClick:
            return False
        else:
            c = self.dial.getchildren()
            click = c[self.currentClick-1].getchildren()
            return click
            return ((click[0].text,  click[0].get("power")), (click[1].text, click[1].get("power")), (click[2].text, click[2].get("power")), (click[3].text, click[3].get("power")))
            
    def getLine(self):
        if self.getClicks()>self.currentClick:
            c = self.dial.getchildren()
            click = c[self.currentClick-1]
            line = click.get("line")
            if line:
                return line
            else:
                return False
            
    def drawDial(self):
        im = Image.new('RGBA', (150, 150),  (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        draw.ellipse( (0, 0, 150, 150 ),  fill="black" )
        
        if self.getRank() == "Unique":
            draw.ellipse( (2, 2, 148, 148 ),  fill="gray" )
            draw.ellipse( (4, 4, 146, 146 ),  fill="black" )
        elif self.getRank() == "LE":
            draw.ellipse( (2, 2, 148, 148 ),  fill="darkkhaki" )
            draw.ellipse( (4, 4, 146, 146 ),  fill="black" )
        
        if self.drawWindow:
            draw.polygon( [(55, 65), (55, 135), (60, 140), (95, 140),  (112, 135), (84, 65)], fill="white")
        
        if ( self.currentClick == 1 ):
            draw.line( ( 57,  67,  57,  133 ),  fill="green", width=2 )
        else:
            line = self.getLine()
            if line:
                draw.line( ( 57,  67,  57,  133 ),  fill=line, width=2 )
            
        click = self.getClick()
        fontPath = "/Library/Fonts/"
        font = ImageFont.truetype(fontPath+"Arial.ttf", 14)
        clickNumFont = ImageFont.truetype(fontPath+"Arial.ttf", 10)
        dialTopFont = ImageFont.truetype(fontPath+"Arial.ttf", 12)
        
        if click == False:
            spd_text = atk_text = def_text = dmg_text = "red"
        else:
            spd_text = atk_text = def_text = dmg_text = "black"
            
        self.currentSpdPower = self.currentAtkPower = self.currentDefPower = self.currentDmgPower = False

        x = 65
        y = 68
        dY = 24
        dX = 13
        
        offset = 0
        if self.currentClick > 9:
            offset = 4
        draw.text( (x+25-offset,  y+dY+9),  str(self.currentClick),  font=clickNumFont,  fill="red")
        draw.text( (11,  45),  self.getName(),  font=dialTopFont,  fill="white" )
        draw.text( (15,  33),  self.getId(),  font=clickNumFont,  fill="white" )

        draw.text( (150-25-(3*len(str(self.getPoints()))), 33),  self.getPoints(),  font=clickNumFont,  fill="white")
            
        r = self.getRange()
        if r:
            draw.text( (102, 68),  r[0],  font=font,  fill="white" )
            for i in range(1, int(r[1])+1):
                im.paste( self.target_image,  (106+(i*6), 68) )
        
        if self.team_symbols and len(self.team_symbols):
            i = 0
            for t in self.team_symbols:
                im.paste( t,  (75-12*len(self.team_symbols)+(24*i), 6))
                i += 1
                
        if click:
            self.drawValues( im, draw,  click,  font )
        else:
            offset = 0
            spd_xy = (x-4, y)
            atk_xy = (x-4,  y+dY)
            def_xy = (x-4,  y+dY+dY)
            dmg_xy = (x+20,  y+dY+dY-1)
            
            draw.text( spd_xy,  "KO",  font=font,  fill="red" )
            draw.text( atk_xy,  "KO",  font=font,  fill="red" )
            draw.text( def_xy,  "KO",  font=font,  fill="red" )
            draw.text( dmg_xy,  "KO",  font=font,  fill="red" )
        
        if self.spd_symbol_image:
            im.paste( self.spd_symbol_image,  ( 31,  65 ) )
        if self.atk_symbol_image:
            im.paste( self.atk_symbol_image,  ( 31,  90 ) )
        if self.def_symbol_image:
            im.paste( self.def_symbol_image,  ( 31,  115 ) )
        if self.dmg_symbol_image:
            im.paste( self.dmg_symbol_image,  ( 109,  106 ) )
        if self.trait_symbol_image:
            im.paste( self.trait_symbol_image,  ( 14,  93 ) )
            
        #print self.trait_symbol_image
        
        #This solution is ignorant, but for some reason Image.tostring can't get PNG data or any format easily understood by QPixmap
        output = StringIO.StringIO()
        im.save(output, "PNG")
        contents = output.getvalue()
        output.close()
        
        return contents
        
    def getToolTip(self, xy):
        x = xy.x()
        y = xy.y()
        if ( x >= self.spd_box[0][0] and x <= self.spd_box[1][0] and y >= self.spd_box[0][1] and y <= self.spd_box[1][1] ):
            return self.describePower("spd", self.currentSpdPower)
        elif ( x >= self.atk_box[0][0] and x <= self.atk_box[1][0] and y >= self.atk_box[0][1] and y <= self.atk_box[1][1] ):
            return self.describePower("atk", self.currentAtkPower)
        elif ( x >= self.def_box[0][0] and x <= self.def_box[1][0] and y >= self.def_box[0][1] and y <= self.def_box[1][1] ):
            return self.describePower("def", self.currentDefPower)
        elif ( x >= self.dmg_box[0][0] and x <= self.dmg_box[1][0] and y >= self.dmg_box[0][1] and y <= self.dmg_box[1][1] ):
            return self.describePower("dmg", self.currentDmgPower)
        elif ( x >= 31 and x <= 54 and y >= 65 and y <= 88 ):
            return self.describeAbility( "spd" )
        elif ( x >= 31 and x <= 54 and y >= 90 and y <= 113 ):
            return self.describeAbility( "atk" )
        elif ( x >= 31 and x <= 54 and y >= 115 and y <= 128 ):
            return self.describeAbility( "def" )
        elif ( x >= 109 and x <= 122 and y >= 106 and y <= 129 ):
            return self.describeAbility( "dmg" )
        elif ( self.traits and x >= 14 and x <= 31 and y >= 93 and y <= 116 ):
            return self.describeTraits()
        elif ( self.teams and y <= 20 and x>= (75-12*len(self.team_symbols)) and x <= (75-12*len(self.team_symbols)+(24*len(self.team_symbols)))):
            return self.describeTeamAbilities()
        elif ( self.keywords and y >= 45 and y <= 58 ):
            return self.describeKeywords()
