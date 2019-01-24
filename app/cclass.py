
import json
from base import Jsonable
from spells import SpellcastingAbility


"""
A player character's (PC) class.
This particular feature is going to be modelled by aggregating
all the class/level combinations to view the PC's class.
This model reflects how the PHB breaks down the class by level,
as well as make multiclassing easier to manage.
i.e. a pure 10th level ranger will have ranger_1, ranger_2,
..., ranger_10 objects. Whereas a barbarian 2/druid 2 PC
will have a total of 4 objects, 2 from each class.
"""
class PlayerClass(Jsonable):

    def __init__(self, name, level, hit_die, proficiencies, saving_throws, skills, features, spellcasting=None):
        self.name = name
        self.level = level
        self.hit_die = hit_die
        self.proficiencies = proficiencies
        self.saving_throws = saving_throws
        self.skills = skills
        self.features = features
        self.spellcasting = spellcasting

    def __json__(self):
        spellcasting_p = self.spellcasting
        if spellcasting_p:
            spellcasting_p = spellcasting_p.__json__()
        j = {
                'class': self.name,
                'level': self.level,
                'hit_die': 'd{}'.format(self.hit_die),
                'proficiencies': self.proficiencies,
                'saving_throws': self.saving_throws,
                'skills': self.skills,
                'features': self.features,
                'spellcasting': spellcasting_p,
            }
        return j

"""
A class factory. This must be extended to accomodate a specific
class. This enforces classes to implement features that
the PC gains upon reaching a specific level.
"""
class PlayerClassFactory(object):
    def __init__(self):
        pass

    def generate_by_level(self, level, **kwargs):
        if level == 1:
            return self._generate_class_1(**kwargs)
        elif level == 2:
            return self._generate_class_2(**kwargs)
        else:
            print('not a valid level!')
            return None

    def _generate_class_1(self):
        pass

    def _req_class_1(self):
        pass

    def _generate_class_2(self):
        pass

    def _req_class_2(self):
        pass


class RangerFactory(PlayerClassFactory):
    def _generate_class_1(self, skills=[], favored_enemy=None, languages=None, favored_terrain=None):
        # validation
        if len(skills) != 3:
            raise ValueError('You must pick 3 skill proficiencies!')

        def_skills = set(['animal_handling', 'athletics', 'insight', 'investigation',
                        'nature', 'perception', 'stealth', 'survival'])
        if not set(skills).issubset(def_skills):
            raise ValueError('You must pick valid skill proficiencies!')

        if not favored_enemy or favored_enemy not in ['aberrations', 'fey', 'elementals', 'plants']:
            raise ValueError('You must select a favored enemy!')
        if not languages:
            raise ValueError('You must select a language!')
        if not favored_terrain or favored_terrain not in ['forest', 'grassland', 'swamp']:
            raise ValueError('You must select a favored terrain!')
  
        def_features = {
                'favored_enemy': {
                    'deescription': 'has a grudge against something',
                    'enemies': [favored_enemy],
                },
                'languages': [languages],
                'natural_explorer': {
                    'description': 'really likes a certain terrain',
                    'terrains': [favored_terrain]
                },
        }
        return Ranger(level=1,
                      skills=skills,
                      features=def_features,
                      spellcasting=None)

    def _req_class_1(self):
        req = {
            'skill_proficiency': {
                'skills': ['animal_handling', 'athletics', 'insight', 'investigation', 'nature', 'perception', 'stealth', 'survival'],
                'choices': 3,
            },
            'favored_enemy': {
                'enemies': ['aberrations', 'fey', 'elementals', 'plants'],
                'choices': 1,
            },
            'languages': {
                'description': 'choose a language based on your favored enemy',
                'choices': 1,
            },
            'favored_terrain': {
                'terrains': ['forest', 'grassland', 'swamp'],
                'choices': 1,
            }
        }
        return req

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

        # TODO make this a bit more elegant...
        spellcasting = SpellcastingAbility(list_spells_known=['hunters_mark', 'cure_wounds'],
                                           spell_slots={ "1st": 2 })
        return Ranger(level=2, skills=[], features=features, spellcasting=spellcasting)

    def _req_class_2(self):
        pass


class Ranger(PlayerClass):
    def __init__(self, level, skills, features, spellcasting):
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
                                      features=features,
                                      spellcasting=spellcasting)
