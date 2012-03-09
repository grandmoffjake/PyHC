from Clix import *

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
        
        self.trait_symbol_image = self.spd_symbol_image = self.atk_symbol_image = self.def_symbol_image = self.dmg_symbol_image = False
        
        self.usePAC = True
        
        self.tokenColor = "red"
        self.tokens = 0
        
        self.target_image = Image.open( os.path.join(sys.path[0], 'images', 'units-targets-1.gif') ).convert('RGB').convert('P', palette=Image.ADAPTIVE)
        
        if self.teams:
            teams = self.teams.getchildren()
            for t in teams:
                self.team_symbols.append(Image.open( os.path.join(sys.path[0], 'images', self.getTeamImage(t.text)) ))
                
        if self.symbols:
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
            
    def drawValues(self, im, draw, click, font):
        x = 65
        y = 68
        dY = 24
        dX = 13
        
        spd_txt = atk_text = def_text = dmg_text = "black"
        
        if click:
            self.currentSpdPower = click[0].get("power")
            self.currentAtkPower = click[1].get("power")
            self.currentDefPower = click[2].get("power")
            self.currentDmgPower = click[3].get("power")

            if self.currentSpdPower == "SPC":
                draw.rectangle( self.spd_box,  outline="black",  fill="white" )
            elif self.currentSpdPower:
                c = self.board.PAC.getColors(self.currentSpdPower)
                spd_text = c[1]
                draw.rectangle( self.spd_box,  fill=c[0] )
        
            if self.currentAtkPower == "SPC":
                draw.rectangle( self.atk_box,  outline="black",  fill="white" )
            elif self.currentAtkPower:
                c = self.board.PAC.getColors(self.currentAtkPower)
                atk_text = c[1]
                draw.rectangle( self.atk_box,  fill=c[0] )
        
            if self.currentDefPower == "SPC":
                draw.rectangle( self.def_box,  outline="black",  fill="white" )
            elif self.currentDefPower:
                c = self.board.PAC.getColors(self.currentDefPower)
                def_text = c[1]
                draw.rectangle( self.def_box,  fill=c[0] )
        
            if self.currentDmgPower == "SPC":
                draw.rectangle( self.dmg_box,  outline="black",  fill="white" )
            elif self.currentDmgPower:
                c = self.board.PAC.getColors(self.currentDmgPower)
                dmg_text = c[1]
                draw.rectangle( self.dmg_box,  fill=c[0] )
        
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
