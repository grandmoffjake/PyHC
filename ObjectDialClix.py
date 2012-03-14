from SingleBaseClix import *

class ObjectDialClix(SingleBaseClix):
    def __init__(self, parent):
        XML = """
        	<object id="IG" name="Infinity Gauntlet" type="dial" points="10" loop="true">
		<rules><![CDATA[<b>Cost</b><br/>Infinity Gauntlet costs 10 points, plus 5 points for each Gem attached to it. At least one Gem must be attached to the gauntlet to activate it. You can't attach more than one of the same type of gem.<br/>
<b>Assign</b><br/>Infinity Gauntlet is assigned to a character when you reveal your force and only that character can use its effects. When assigned character is KO'd, opponent scores the Infinity Gauntlet.<br/>
<b>Setup</b><br/>Infinity Gauntlet dial begins on the green line, but does not have a KO click; the dial may rotate past the starting line. You may not add special objects to your force if Infinity Gauntlet is part of it.<br/>
<b>Turning the Dial</b><br/>At the end of your turn, if assigned character was given a non-free action this turn, choose one: 1) deal assigned character 1 unavoidable damage; or 2) roll a d6 that can't be rerolled and turn the Infinity Gauntlet dial to the right that many times; or 3) if Infinity Gauntlet dial has a special power visible, you may choose to do nothing.<br/>
<b>Using Effects</b><br/>When a Gem, a standard power or a special power is revealed on the dial, assigned character can use the effects associated with that if they can't already. You may only use the Gem effects if that Gem is attached.<br/>
<b>THE GAUNTLET COMPLETE</b><br/>If all six Gems are attached, character's powers and combat abilities can't be countered and character can use Willpower.<br/>
		]]></rules>
		<specials>
			<special power="ONE" name="BEYOND MORTAL LIMITS" color="special" shape="circle">At the beginning of your turn, choose an attached gem that you did not choose during your last turn. Character can use the effects of that gem as long as this power is showing.</special>
			<special power="TWO" name="APOTHEOSIS APPROACHING" color="special" shape="circle">Modify character's combat values by +1. At the beginning of your turn, choose a standard power character can't already use. Character can use that power until your next turn.</special>
			<special power="THREE" name="ULTIMATE GODHOOD ATTAINED" color="special" shape="circle">Modify character's combat values by +2 and character can use the effects of every attached gem. At the beginning of your turn, choose a standard power character can't already use. Character can use that power until your next turn.</special>
			<special power="SOULGEM" name="SOUL GEM" color="green" shape="circle">Character can use Steal Energy. When character KO's an opposing character, heal character of 2 damage.</special>
			<special power="POWERGEM" name="POWER GEM" color="red" shape="circle">If character's printed range value is 4 or less, character can use Close Combat Expert. If character's range value is 5 or more, character can use Ranged Combat Expert.</special>
			<special power="TIMEGEM" name="TIME GEM" color="orange" shape="circle">Character can use Incapacitate and Super Senses.</special>
			<special power="SPACEGEM" name="SPACE GEM" color="purple" shape="circle">Character can use Phasing/Teleport and the Carry ability. Modify character's speed value by +2.</special>
			<special power="REALITYGEM" name="REALITY GEM" color="yellow" shape="circle">Character can use Probability Control, but only during character's turn.</special>
			<special power="MINDGEM" name="MIND GEM" color="lightblue" shape="circle">Character can use Mind Control and Telekinesis.</special>
		</specials>
		<dial length="26">
			<click num="1">
				<spd power="SPACEGEM"/>
				<atk power="TIMEGEM"/>
				<def power="POWERGEM"/>
				<dmg power="TK" type="PAC">A</dmg>
			</click>
			<click num="2">
				<spd power="REALITYGEM"/>
				<atk power="SOULGEM"/>
				<def power="TIMEGEM"/>
				<dmg power="LC" type="PAC">S</dmg>
			</click>
			<click num="3">
				<spd power="MINDGEM"/>
				<atk power="POWERGEM"/>
				<def power="SPACEGEM"/>
				<dmg power="MM" type="PAC">D</dmg>
			</click>
			<click num="4">
				<spd power="SOULGEM"/>
				<atk power="TIMEGEM"/>
				<def power="REALITYGEM"/>
				<dmg power="MC" type="PAC">S</dmg>
			</click>
			<click num="5">
				<spd power="POWERGEM"/>
				<atk power="SOULGEM"/>
				<def power="MINDGEM"/>
				<dmg power="CHG" type="PAC">S</dmg>
			</click>
			<click num="6">
				<spd power="MINDGEM"/>
				<atk power="POWERGEM"/>
				<def power="SOULGEM"/>
				<dmg power="SSE" type="PAC">D</dmg>
			</click>
			<click num="7">
				<spd power="SOULGEM"/>
				<atk power="TIMEGEM"/>
				<def power="MINDGEM"/>
				<dmg power="STL" type="PAC">S</dmg>
			</click>
			<click num="8">
				<spd power="POWERGEM"/>
				<atk power="SPACEGEM"/>
				<def power="REALITYGEM"/>
				<dmg power="BCF" type="PAC">A</dmg>
			</click>
			<click num="9">
				<spd power="TIMEGEM"/>
				<atk power="REALITYGEM"/>
				<def power="SOULGEM"/>
				<dmg power="QK" type="PAC">A</dmg>
			</click>
			<click num="10">
				<spd power="SPACEGEM"/>
				<atk power="MINDGEM"/>
				<def power="POWERGEM"/>
				<dmg power="POI" type="PAC">A</dmg>
			</click>
			<click num="11">
				<spd power="REALITYGEM"/>
				<atk power="SOULGEM"/>
				<def power="TIMEGEM"/>
				<dmg power="COM" type="PAC">D</dmg>
			</click>
			<click num="12">
				<spd power="MINDGEM"/>
				<atk power="POWERGEM"/>
				<def power="SPACEGEM"/>
				<dmg power="PB" type="PAC">A</dmg>
			</click>
			<click num="13">
				<spd power="SOULGEM"/>
				<atk power="TIMEGEM"/>
				<def power="REALITYGEM"/>
				<dmg power="FLR" type="PAC">S</dmg>
			</click>
			<click num="14">
				<spd power="POWERGEM"/>
				<atk power="SPACEGEM"/>
				<def power="MINDGEM"/>
				<dmg power="ESD" type="PAC">D</dmg>
			</click>
			<click num="15">
				<spd power="TIMEGEM"/>
				<atk power="REALITYGEM"/>
				<def power="ONE">1</def>
				<dmg power="CCE" type="PAC">G</dmg>
			</click>
			<click num="16">
				<spd power="SPACEGEM"/>
				<atk power="MINDGEM"/>
				<def power="ONE">1</def>
				<dmg power="EW" type="PAC">G</dmg>
			</click>
			<click num="17">
				<spd power="REALITYGEM"/>
				<atk power="SPACEGEM"/>
				<def power="ONE">1</def>
				<dmg power="RCE" type="PAC">G</dmg>
			</click>
			<click num="18">
				<spd power="MINDGEM"/>
				<atk power="REALITYGEM"/>
				<def power="ONE">1</def>
				<dmg power="TOU" type="PAC">D</dmg>
			</click>
			<click num="19">
				<spd power="SOULGEM"/>
				<atk power="MINDGEM"/>
				<def power="ONE">1</def>
				<dmg power="INV" type="PAC">D</dmg>
			</click>
			<click num="20">
				<spd power="POWERGEM"/>
				<atk power="SOULGEM"/>
				<def power="ONE">1</def>
				<dmg power="IMP" type="PAC">D</dmg>
			</click>
			<click num="21">
				<spd power="TIMEGEM"/>
				<atk power="POWERGEM"/>
				<def power="SOULGEM"/>
				<dmg power="TWO">2</dmg>
			</click>
			<click num="22">
				<spd power="SPACEGEM"/>
				<atk power="TIMEGEM"/>
				<def power="POWERGEM"/>
				<dmg power="TWO">2</dmg>
			</click>
			<click num="23">
				<spd power="REALITYGEM"/>
				<atk power="SPACEGEM"/>
				<def power="TIMEGEM"/>
				<dmg power="TWO">2</dmg>
			</click>
			<click num="24">
				<spd power="MINDGEM"/>
				<atk power="REALITYGEM"/>
				<def power="SPACEGEM"/>
				<dmg power="TWO">2</dmg>
			</click>
			<click num="25">
				<spd power="THREE">3</spd>
				<atk/>
				<def/>
				<dmg/>
			</click>
			<click num="26">
				<spd power="THREE">3</spd>
				<atk/>
				<def/>
				<dmg/>
			</click>
		</dial>
	</object>
    """
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
        if self.specials:
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
            
            if click[0].get("type") == "PAC":
                c = self.board.PAC.getColors(self.currentSpdPower)
                spd_text = c[1]
                draw.rectangle( self.spd_box,  fill=c[0] )
            elif self.currentSpdPower:
                c = self.getColors(self.currentSpdPower)
                spd_text = c[1]
                if c[2] == "circle":
                    if c[0] == "special":
                        draw.ellipse( self.spd_box,  fill="white",  outline="black" )
                    else:
                        draw.ellipse( self.spd_box,  fill=c[0])
                else:
                    draw.rectangle( self.spd_box,  fill=c[0] )
                    
            if click[1].get("type") == "PAC":
                c = self.board.PAC.getColors(self.currentAtkPower)
                atk_text = c[1]
                draw.rectangle( self.atk_box,  fill=c[0] )
            elif self.currentAtkPower:
                c = self.getColors(self.currentAtkPower)
                atk_text = c[1]
                if c[2] == "circle":
                    if c[0] == "special":
                        draw.ellipse( self.atk_box,  fill="white",  outline="black" )
                    else:
                        draw.ellipse( self.atk_box,  fill=c[0])
                else:
                    draw.rectangle( self.atk_box,  fill=c[0] )
                    
            if click[2].get("type") == "PAC":
                c = self.board.PAC.getColors(self.currentDefPower)
                def_text = c[1]
                draw.rectangle( self.def_box,  fill=c[0] )
            elif self.currentDefPower:
                c = self.getColors(self.currentDefPower)
                def_text = c[1]
                if c[2] == "circle":
                    if c[0] == "special":
                        draw.ellipse( self.def_box,  fill="white",  outline="black" )
                    else:
                        draw.ellipse( self.def_box,  fill=c[0])
                else:
                    draw.rectangle( self.def_box,  fill=c[0] )
                    
            if click[3].get("type") == "PAC":
                c = self.board.PAC.getColors(self.currentDmgPower)
                dmg_text = c[1]
                draw.rectangle( self.dmg_box,  fill=c[0] )
            elif self.currentDmgPower:
                c = self.getColors(self.currentDmgPower)
                dmg_text = c[1]
                if c[2] == "circle":
                    if c[0] == "special":
                        draw.ellipse( self.dmg_box,  fill="white",  outline="black" )
                    else:
                        draw.ellipse( self.dmg_box,  fill=c[0])
                else:
                    draw.rectangle( self.dmg_box,  fill=c[0] )
                                
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
