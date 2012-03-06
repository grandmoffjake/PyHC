import xml.etree.ElementTree as ET
import Image
import ImageDraw
import StringIO

class Clix:
    def __init__(self, parent):
        XML = """
        <figure id="mnm002" name="Cyclops" rank="Rookie" team="X-Men" range="8" targets="1" points="50">
            <symbols>
                <spd>Boot</spd>
                <atk>Fist</atk>
                <def>Shield</def>
                <dmg>Star</dmg>
            </symbols>
            <specials>
                <spd>
                    <name>Concusive Blast</name>
                    <description><![CDATA[When Cyclops makes a ranged combat attack and deals damage to an opposing character, the character is knocked back equal to the damage dealt.]]></description>
                </spd>
            </specials>
            <dial length="6">
                <click num="1">
                    <spd power="RS">8</spd>
                    <atk>9</atk>
                    <def>17</def>
                    <dmg>3</dmg>
                </click>
                <click num="2">
                    <spd power="SPC">8</spd>
                    <atk power="EE">10</atk>
                    <def power="WIL">16</def>
                    <dmg>2</dmg>
                </click>
                <click num="3">
                    <spd power="SPC">7</spd>
                    <atk>10</atk>
                    <def power="WIL">16</def>
                    <dmg power="RCE">2</dmg>
                </click>
                <click num="4">
                    <spd>7</spd>
                    <atk>9</atk>
                    <def>15</def>
                    <dmg power="RCE">2</dmg>
                </click>
                <click num="5">
                    <spd>7</spd>
                    <atk>8</atk>
                    <def>14</def>
                    <dmg power="RCE">1</dmg>
                </click>
                <click num="6">
                    <spd>6</spd>
                    <atk>7</atk>
                    <def>13</def>
                    <dmg>1</dmg>
                </click>
            </dial>
        </figure>"""
        self.xmlDial = ET.fromstring(XML)
        self.dial = self.xmlDial.find("dial")
        self.symbols = self.xmlDial.find("symbols")
        self.specials = self.xmlDial.find("specials")
        self.traits = self.xmlDial.find("traits")
        self.board = parent
        self.currentClick = 1
        return 
        
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
            
    def damage(self):
        if self.currentClick < self.getClicks()+1:
            self.currentClick += 1
            
    def describePower(self, position, code):
        if code == "SPC":
            c = self.specials.find(position)
            return c.findtext("name") + " - " + c.findtext("description")
        else:
            return self.board.PAC.getDescription(code)

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
        draw.rectangle( (10, 10, 90, 90 ),  fill="yellow",  outline="red" )
        
        #This solution is ignorant, but for some reason Image.tostring can't get PNG data or any format easily understood by QPixmap
        output = StringIO.StringIO()
        im.save(output, "PNG")
        contents = output.getvalue()
        output.close()
        
        return contents
