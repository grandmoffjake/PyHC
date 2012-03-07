class PAC:
    def __init__(self):
        self.colors = {
            #Color: Background, Foreground
            "gray": ("#444","#fff")
        }
        self.powers = {
            #POWER: (Name,Description,RGB_Background,RGB_Foreground)
            "RS": ("Running Shot", "Give this character a power action; halve its speed value for the action. Move this character up to its speed value and it may be given a ranged combat action as a free action.", "gray")
        }
        return
        
    def getDescription(self, power):
        return self.powers[power][0]+" - "+"Give this character a power action; halve its speed value for the action. Move this character up to its speed value and it may be given a ranged combat action as a free action."
        
    def getColor(self, power):
        return self.colors[self.powers[power][3]]
