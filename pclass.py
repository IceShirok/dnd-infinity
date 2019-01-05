
import json
from base import Jsonable

class PlayerClass(Jsonable):

    def __init__(self, name, level, hit_die, proficiencies, saving_throws, skills, features):
        self.name = name
        self.level = level
        self.hit_die = hit_die
        self.proficiencies = proficiencies
        self.saving_throws = saving_throws
        self.skills = skills
        self.features = features

    def __json__(self):
        j = {
                'class': self.name,
                'level': self.level,
                'hit_die': 'd{}'.format(self.hit_die),
                'proficiencies': self.proficiencies,
                'saving_throws': self.saving_throws,
                'skills': self.skills,
                'features': self.features,
            }
        return j

class PlayerClassFactory(object):
    def __init__(self):
        pass

    def generate_by_level(self, level):
        if level == 1:
            return self._generate_class_1()
        elif level == 2:
            return self._generate_class_2()
        else:
            print('not a valid level!')
            return None

    def _generate_class_1(self):
        pass

    def _generate_class_2(self):
        pass

class RangerFactory(PlayerClassFactory):
    def _generate_class_1(self):
        def_skills = ['animal_handling', 'athletics', 'insight', 'investigation',
                        'nature', 'perception', 'stealth', 'survival']
        def_features = {
                'favored_enemy': {
                    'deescription': 'has a grudge against something',
                },
                'natural_explorer': {
                    'description': 'really likes a certain terrain',
                },
        }
        return Ranger(level=1,
                      skills=def_skills,
                      features=def_features)

    def _generate_class_2(self):
        features = {
                'fighting_style': {
                    'styles': ['archery', 'defense', 'dueling', 'two_weapon_fighting'],
                    'choices': 1,
                },
                'spellcasting': {
                    'spellcasting_ability': 'WIS',
                    'spells_known': 2,
                    'spell_slots': {
                        '1st': 2
                    }
                }
        }
        return Ranger(level=2, skills=[], features=features)

class Ranger(PlayerClass):
    def __init__(self, level, skills, features):
        super(Ranger, self).__init__(name='Ranger',
                                          level=level,
                                          hit_die=10,
                                          proficiencies={
                                              'armor': ['light', 'medium', 'shields'],
                                              'weapons': ['simple', 'martial'],
                                              'tools': [],
                                          },
                                          saving_throws=['STR', 'DEX'],
                                          skills=skills,
                                          features=features)

