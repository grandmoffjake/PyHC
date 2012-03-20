from SingleBaseClix import *

class ObjectDialClix(SingleBaseClix):
    def __init__(self, parent, XML):
        SingleBaseClix.__init__(self, parent, XML)
        self.dial = self.xmlDial.find("dial")
        self.specials = self.xmlDial.find("specials")
        self.rules = self.xmlDial.find("rules")
        self.tokens = 0
        self.active = 0
        self.mine = True
        
        if self.rules != False:
            self.traits = True
            self.trait_symbol_image = Image.open( os.path.join(sys.path[0], 'images', 'trait-star.gif') ).convert('RGB').convert('P', palette=Image.ADAPTIVE)
        
        self.powers = {}
        if self.specials is not None:
            for s in self.specials:
                self.powers[s.get("power")] = s
                
    def takeObject(self, o):
        return False
        
    def describeAbility(self, ability):
        return
        
    def describeTraits(self):
        if self.traits:
            return self.rules.text
        return ""
        
    def damage(self):
        if self.xmlDial.get("loop") == "true":
            if self.currentClick < self.getClicks():
                self.currentClick += 1
            else:
                self.currentClick = 1
            self.board.log( "Me", self.getName() + " was turned 1 click." )
        else:
            if self.currentClick < self.getClicks()+1:
                self.currentClick += 1
                self.board.log( "Me", self.getName() + " was turned 1 click." )
        
    def describePower(self, position, code):
        click = self.getClick()
        
        if code in self.powers and self.powers[code].get("name") and self.powers[code].text:
            return "<b>"+self.powers[code].get("name") + "</b><br/>" + self.powers[code].text
        else:
            if position == "spd" and click[1].get("type") == "PAC":
                return self.board.PAC.getDescription(code)
            elif position == "dmg" and click[3].get("type") == "PAC":
                return self.board.PAC.getDescription(code)
        return ""
        
    def token(self, color):
        return
        
    def getColors(self, power):
        if power:
            text = self.powers[power].get("text")
            if not text:
                text = "black"
            return (self.powers[power].get("color"), text, self.powers[power].get("shape"))
        
    def drawValues(self, im, draw, click, font, xOffset):
        x = 65+xOffset
        y = 68
        dY = 24
        dX = 13
        
        spd_txt = atk_text = def_text = dmg_text = "black"
        
        spd_box = [(60+xOffset, 67), (78+xOffset, 85)]
        atk_box = [(60+xOffset, 90), (78+xOffset, 108)]
        def_box = [(60+xOffset, 115), (78+xOffset, 133)]
        dmg_box = [(83+xOffset, 114), (101+xOffset, 132)]
        
        if click:
            self.currentSpdPower = click[0].get("power")
            self.currentAtkPower = click[1].get("power")
            self.currentDefPower = click[2].get("power")
            self.currentDmgPower = click[3].get("power")
            
            if click[0].get("type") == "PAC":
                c = self.board.PAC.getColors(self.currentSpdPower)
                spd_text = c[1]
                draw.rectangle( spd_box,  fill=c[0] )
            elif self.currentSpdPower:
                c = self.getColors(self.currentSpdPower)
                spd_text = c[1]
                if c[2] == "circle":
                    if c[0] == "special":
                        draw.ellipse( spd_box,  fill="white",  outline="black" )
                    else:
                        draw.ellipse( spd_box,  fill=c[0])
                else:
                    draw.rectangle( spd_box,  fill=c[0] )
                    
            if click[1].get("type") == "PAC":
                c = self.board.PAC.getColors(self.currentAtkPower)
                atk_text = c[1]
                draw.rectangle( atk_box,  fill=c[0] )
            elif self.currentAtkPower:
                c = self.getColors(self.currentAtkPower)
                atk_text = c[1]
                if c[2] == "circle":
                    if c[0] == "special":
                        draw.ellipse( atk_box,  fill="white",  outline="black" )
                    else:
                        draw.ellipse( atk_box,  fill=c[0])
                else:
                    draw.rectangle( atk_box,  fill=c[0] )
                    
            if click[2].get("type") == "PAC":
                c = self.board.PAC.getColors(self.currentDefPower)
                def_text = c[1]
                draw.rectangle( def_box,  fill=c[0] )
            elif self.currentDefPower:
                c = self.getColors(self.currentDefPower)
                def_text = c[1]
                if c[2] == "circle":
                    if c[0] == "special":
                        draw.ellipse( def_box,  fill="white",  outline="black" )
                    else:
                        draw.ellipse( def_box,  fill=c[0])
                else:
                    draw.rectangle( def_box,  fill=c[0] )
                    
            if click[3].get("type") == "PAC":
                c = self.board.PAC.getColors(self.currentDmgPower)
                dmg_text = c[1]
                draw.rectangle( dmg_box,  fill=c[0] )
            elif self.currentDmgPower:
                c = self.getColors(self.currentDmgPower)
                dmg_text = c[1]
                if c[2] == "circle":
                    if c[0] == "special":
                        draw.ellipse( dmg_box,  fill="white",  outline="black" )
                    else:
                        draw.ellipse( dmg_box,  fill=c[0])
                else:
                    draw.rectangle( dmg_box,  fill=c[0] )
                                
        offset = 0
        if click[0].text and len(click[0].text) > 1:
            offset = 4
        spd_xy = (x-offset, y)
        
        offset = 0
        if click[1].text and len(click[1].text) > 1:
            offset = 4
        atk_xy = (x-offset,  y+dY)
        
        offset = 0
        if click[2].text and len(click[2].text) > 1:
            offset = 4
        def_xy = (x-offset,  y+dY+dY)
        
        offset = 0
        if click[3].text and len(click[3].text) > 1:
            offset = 4
        dmg_xy = (x+24-offset,  y+dY+dY-1)
        
        if click[0].text:
            draw.text( spd_xy,  click[0].text,  font=font,  fill="black" )
        if click[1].text:
            draw.text( atk_xy,  click[1].text,  font=font,  fill=atk_text )
        if click[2].text:
            draw.text( def_xy,  click[2].text,  font=font,  fill=def_text )
        if click[3].text:
            draw.text( dmg_xy,  click[3].text,  font=font,  fill=dmg_text )
        
        return draw
