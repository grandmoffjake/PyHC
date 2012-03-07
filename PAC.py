import xml.etree.ElementTree as ET
import os, sys

class PAC:
    def __init__(self):
        self.xml = ET.parse(os.path.join(sys.path[0], 'assets', 'PAC.xml'))
        powers = self.xml.find("powers").getchildren()
        abilities = self.xml.find("abilities").getchildren()
        self.powers = {}
        self.abilities = {}
        for p in powers:
            self.powers[p.get("code")] = p.items()
        for p in abilities:
            self.abilities[p.get("code")] = p.text
            
        #print self.powers
        
    def getDescription(self, power):
        return "<b>"+self.powers[power][1][1]+"</b><br/>"+self.powers[power][5][1]
        
    def getAbilityDescription(self, ability):
        if ability in self.abilities:
            return self.abilities[ability]
            
        return ""
        
    def getColors(self, power):
        return (self.powers[power][2][1],self.powers[power][3][1])
