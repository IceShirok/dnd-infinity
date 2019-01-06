
import json
from base import Jsonable


"""
A player character's (PC) background.
This doesn't change after a PC is created, but this is created
separately because it is a separate section in the PHB and is
easy to model as such.
"""
class PlayerBackground(Jsonable):

    def __init__(self, name, feature, proficiencies, languages):
        self.name = name
        self.feature = feature
        self.proficiencies = proficiencies
        self.languages = languages

    def __json__(self):
        j = {
                'background': self.name,
                'feature': self.feature,
                'proficiencies': self.proficiencies,
                'languages': self.languages,
        }
        return j

class Criminal(PlayerBackground):
    def __init__(self):
        super(Criminal, self).__init__(name='criminal',
                                                 feature={
                                                    'name': 'criminal contact',
                                                    'description': 'You have an accomplice.',
                                                 },
                                                 proficiencies={
                                                     'skills': ['deception', 'stealth'],
                                                     'tools': ['thieves_tools', 'bone_dice'],
                                                 },
                                                 languages=[])


