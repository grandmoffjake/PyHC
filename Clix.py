import xml.etree.ElementTree as ET
import Image
import ImageDraw
import ImageFont
import StringIO
import os
import sys

class Clix:
    def __init__(self, parent):
        XML = """
        <figure id="mnm020" name="Morph" rank="Experienced" team="X-Men" range="0" targets="1" points="90"><symbols><spd>Wing</spd><atk>Fist</atk><def>Shield</def><dmg>Star</dmg></symbols><specials><atk><name>Omnimorph</name><description><![CDATA[Morph can use Perplex, but he can target only himself.]]></description></atk></specials><dial length="7"><click num="1"><spd power="CHG">9</spd><atk power="SPC">9</atk><def power="TOU">16</def><dmg power="SC">2</dmg></click><click num="2"><spd power="PLA">8</spd><atk power="SPC">9</atk><def power="COM">16</def><dmg power="SC">2</dmg></click><click num="3"><spd power="CHG">8</spd><atk power="SPC">9</atk><def power="TOU">16</def><dmg power="SC">2</dmg></click><click num="4"><spd power="CHG">8</spd><atk power="SPC">8</atk><def power="COM">16</def><dmg power="SC">2</dmg></click><click num="5"><spd power="PLA">7</spd><atk power="SPC">8</atk><def power="COM">15</def><dmg power="SC">2</dmg></click><click num="6"><spd power="PLA">7</spd><atk power="SPC">7</atk><def power="REG">14</def><dmg power="SC">2</dmg></click><click num="7"><spd>6</spd><atk>6</atk><def power="REG">14</def><dmg power="SC">2</dmg></click></dial></figure>
        """
        self.xmlDial = ET.fromstring(XML)
        self.dial = self.xmlDial.find("dial")
        self.symbols = self.xmlDial.find("symbols")
        self.specials = self.xmlDial.find("specials")
        self.traits = self.xmlDial.find("traits")
        self.teams = self.xmlDial.find("teams")
        self.keywords = self.xmlDial.find("keywords")
        self.team_symbols = []
        self.board = parent
        self.currentClick = 1
        
        self.tokenColor = "red"
        self.tokens = 0
        
        self.spd_box = [(60, 67), (78, 85)]
        self.atk_box = [(60, 90), (78, 108)]
        self.def_box = [(60, 115), (78, 133)]
        self.dmg_box = [(83, 114), (101, 132)]
        
        self.currentSpdPower = False
        self.currentAtkPower = False
        self.currentDefPower = False
        self.currentDmgPower = False
        
        images_path = os.path.join(sys.path[0], 'images')
        
        self.target_image = Image.open( os.path.join(sys.path[0], 'images', 'units-targets-1.gif') ).convert('RGB').convert('P', palette=Image.ADAPTIVE)
        
        if self.teams:
            teams = self.teams.getchildren()
            for t in teams:
                self.team_symbols.append(Image.open( os.path.join(sys.path[0], 'images', self.getTeamImage(t.text)) ))
                
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
        return 
        
    def getTeamImage(self, team):
        if team == "X-Men":
            return "units-ta-xmen-a.gif"
        else:
            return "units-ta-supermanenemy.png"
        
    def getId(self):
        return self.xmlDial.get("id")
        
    def getRange(self):
        return (self.xmlDial.get("range"), self.xmlDial.get("targets"))
        
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
            
    def getClick(self):
        if self.getClicks()<self.currentClick:
            return (("KO", None), ("KO", None), ("KO", None), ("KO", None))
        else:
            c = self.dial.getchildren()
            click = c[self.currentClick-1].getchildren()
            return ((click[0].text,  click[0].get("power")), (click[1].text, click[1].get("power")), (click[2].text, click[2].get("power")), (click[3].text, click[3].get("power")))
            
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

        draw.polygon( [(55, 65), (55, 135), (60, 140), (95, 140),  (112, 135), (84, 65)], fill="white")
        
        if ( self.currentClick == 1 ):
            draw.line( ( 57,  67,  57,  133 ),  fill="green", width=2 )
            
            
        SPD,  ATK,  DEF,  DMG = self.getClick()
        fontPath = "/Library/Fonts/"
        font = ImageFont.truetype(fontPath+"Arial.ttf", 14)
        clickNumFont = ImageFont.truetype(fontPath+"Arial.ttf", 10)
        dialTopFont = ImageFont.truetype(fontPath+"Arial.ttf", 12)
        
        
        if ( SPD[0] == "KO" ):
            spd_text = atk_text = def_text = dmg_text = "red"
        else:
            spd_text = atk_text = def_text = dmg_text = "black"
            self.currentSpdPower = SPD[1]
            self.currentAtkPower = ATK[1]
            self.currentDefPower = DEF[1]
            self.currentDmgPower = DMG[1]
        
        x = 65
        y = 68
        dY = 24
        dX = 13
        
        
        
        if SPD[1]:
            if SPD[1] == "SPC":
                draw.rectangle( self.spd_box,  outline="black",  fill="white" )
            else:
                c = self.board.PAC.getColors(SPD[1])
                spd_text = c[1]
                draw.rectangle( self.spd_box,  fill=c[0] )
        if ATK[1]:
            if ATK[1] == "SPC":
                draw.rectangle( self.atk_box,  outline="black",  fill="white" )
            else:
                c = self.board.PAC.getColors(ATK[1])
                atk_text = c[1]
                draw.rectangle( self.atk_box,  fill=c[0] )
        if DEF[1]:
            if DEF[1] == "SPC":
                draw.rectangle( self.def_box,  outline="black",  fill="white" )
            else:
                c = self.board.PAC.getColors(DEF[1])
                def_text = c[1]
                draw.rectangle( self.def_box,  fill=c[0] )
        if DMG[1]:
            if DMG[1] == "SPC":
                draw.rectangle( self.dmg_box,  outline="black",  fill="white" )
            else:
                c = self.board.PAC.getColors(DMG[1])
                dmg_text = c[1]
                draw.rectangle( self.dmg_box,  fill=c[0] )
        
        offset = 0
        if len(SPD[0]) > 1:
            offset = 4
        spd_xy = (x-offset, y)
        
        offset = 0
        if len(ATK[0]) > 1:
            offset = 4
        atk_xy = (x-offset,  y+dY)
        
        offset = 0
        if len(DEF[0]) > 1:
            offset = 4
        def_xy = (x-offset,  y+dY+dY)
        
        offset = 0
        if len(DMG[0]) > 1:
            offset = 4
        dmg_xy = (x+24-offset,  y+dY+dY-1)
        
        draw.text( spd_xy,  SPD[0],  font=font,  fill=spd_text )
        draw.text( atk_xy,  ATK[0],  font=font,  fill=atk_text )
        draw.text( def_xy,  DEF[0],  font=font,  fill=def_text )
        draw.text( dmg_xy,  DMG[0],  font=font,  fill=dmg_text )
        offset = 0
        if self.currentClick > 9:
            offset = 4
        draw.text( (x+25-offset,  y+dY+9),  str(self.currentClick),  font=clickNumFont,  fill="red")
        draw.text( (11,  45),  self.getName(),  font=dialTopFont,  fill="white" )
        r = self.getRange()
        draw.text( (15,  33),  self.getId(),  font=clickNumFont,  fill="white" )
        draw.text( (150-25-(3*len(str(self.getPoints()))), 33),  self.getPoints(),  font=clickNumFont,  fill="white")
        draw.text( (102, 68),  r[0],  font=font,  fill="white" )
        for i in range(1, int(r[1])+1):
            im.paste( self.target_image,  (106+(i*6), 68) )
        
        if len(self.team_symbols):
            i = 0
            for t in self.team_symbols:
                im.paste( t,  (75-12*len(self.team_symbols)+(24*i), 6))
                i += 1
        
        im.paste( self.spd_symbol_image,  ( 31,  65 ) )
        im.paste( self.atk_symbol_image,  ( 31,  90 ) )
        im.paste( self.def_symbol_image,  ( 31,  115 ) )
        im.paste( self.dmg_symbol_image,  ( 109,  106 ) )
        if self.traits:
            im.paste( self.trait_symbol_image,  ( 14,  93 ) )
        
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
