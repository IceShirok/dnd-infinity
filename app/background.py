
import json
from base import Jsonable

import ability_scores, skills

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
        self.__proficiencies = proficiencies
        self.languages = languages

    def __json__(self):
        j = {
                'background': self.name,
                'feature': self.feature,
                'proficiencies': self.__proficiencies,
                'languages': self.languages,
        }
        return j

    @property
    def skills(self):
        return self.__proficiencies['skills']

    @property
    def background_proficiencies(self):
        p = { **self.__proficiencies }
        return p

    @property
    def proficiencies(self):
        p = { **self.background_proficiencies }
        p.pop('skills')
        return p

class Criminal(PlayerBackground):
    def __init__(self):
        feature = {
            'criminal_contact': {
                'name': 'Criminal Contact',
                'description': 'You have a reliable and trustworthy contact who acts as your liaison to a network of other criminals. ...',
            }
        }
        proficiencies = {
            'skills': [skills.DECEPTION, skills.STEALTH],
            'tools': ['thieves_tools', 'bone_dice'],
        }
        super(Criminal, self).__init__(name='criminal',
                                       feature=feature,
                                       proficiencies=proficiencies,
                                       languages=[])


