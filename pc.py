
from base import Jsonable


"""
A player character (PC) in D&D.
A PC consists of some base characteristics, a race, a class, and
a background.
"""
class PlayerCharacter(Jsonable):
    def __init__(self, base, race=None, classes=None, background=None):
        self.base = base
        self.race = race
        self.classes = classes
        self.background = background

    def __json__(self):
        j_classes = []
        for c in self.classes:
            j_classes.append(c.__json__())
        j = self.base.__json__()
        j['classes'] = j_classes

        if self.race:
            j['race'] = self.race.__json__()
        
        if self.background:
            j['background'] = self.background.__json__()
    
        return j

