
import json
from base import Jsonable


"""
A player character's (PC) race.
A PC's race does not change for the most part, although
some features may scale up with a PC's level.
"""
class Race(Jsonable):
    def __init__(self, name, asi, size, speed, languages=['common'], traits={}):
        self.name = name
        self.asi = asi
        self.size = size
        self.speed = speed
        self.languages = languages
        self.traits = traits
        
        self._verify()

    def __json__(self):
        j = {
                'race': self.name,
                'ability_score_increase': self.asi,
                'size': self.size,
                'speed': self.speed,
                'languages': self.languages,
                'traits': self.traits,
            }
        return j
    
    def _required_customization(self):
        """
        Return a list of features that need to be fulfilled in order for
        the verify function to not spit out fire and brimstone.
        This should be a list of JSON objects.
        """
        return []

    def _verify(self):
        """
        This function serves to make sure that the race, with its inputs,
        is considered valid. In most cases, this applies for races that
        requires selecting a feature amongst a selection (i.e. select a
        skill proficiency from a list of 3).
        Return true if all verification has passed, or throw an exception
        (ValueError?) with a message saying what is invalid.
        """
        return True

# DWARF

class Dwarf(Race):
    def __init__(self, asi, traits):
        def_asi = {'CON': 2}
        def_traits = {
                'darkvision': 60,
                'dwarven_resilience': {
                    'description': 'poison resistance',
                },
                'dwarven_combat_training': {
                    'weapon_proficiency': ['battleaxe', 'handaxe'],
                },
                'stonecunning': {
                    'description': '+10 int checks to stone',
                },
            }
        super(Dwarf, self).__init__(name='Dwarf',
                                    asi={**def_asi, **asi},
                                    size='medium',
                                    speed=25,
                                    languages=['common', 'dwarvish'],
                                    traits={**def_traits, **traits})
    
    def _required_customization(self):
        req = [
            {
                'tool_proficiency': {
                    'tools': ['smiths_tools', 'brewers_kit', 'masons_tools'],
                    'choice': 1,
                }
            }
        ]
        return req

    def _verify(self):
        # TODO try to de-dupe a lot of this proficiency stuff
        if 'tool_proficiency' not in self.traits:
            raise ValueError('Must input a tool proficiency!')
        if self.traits['tool_proficiency'] not in ['smiths_tools', 'brewers_kit', 'masons_tools']:
            raise ValueError('Must enter a valid tool proficiency!')
        return True


class HillDwarf(Dwarf):
    def __init__(self, traits):
        def_asi = {'CON': 2}
        def_traits = {
                          'dwarven_toughness': {
                              'description': 'increase 1 HP per level',
                          },
                      }
        super(HillDwarf, self).__init__(asi=def_asi,
                                        traits={**def_traits, **traits})
        self.name = 'Hill Dwarf'


# GNOME

class Gnome(Race):
    def __init__(self, asi, traits):
        def_asi = {'INT': 2}
        def_traits = {
                'darkvision': 60,
                'gnome_cunning': {
                    'description': 'advantage to all INT, WIS, CHA saving throws against magic',
                },
            }
        super(Gnome, self).__init__(name='Gnome',
                                    asi={**def_asi, **asi},
                                    size='small',
                                    speed=25,
                                    languages=['common', 'gnomish'],
                                    traits={**def_traits, **traits})

class RockGnome(Gnome):
    def __init__(self, traits):
        super(RockGnome, self).__init__(asi={'CON': 1},
                                            traits={
                                                'artificers_lore': {
                                                    'description': '+10 INT checks to magic items',
                                                },
                                                'tinker': {
                                                    'description': 'you have proficiency with tinkers tools',
                                                }
                                            })
        self.name = 'Rock Gnome'


# HUMAN

class Human(Race):
    def __init__(self, languages):
        def_asi = {'STR': 1, 'DEX': 1, 'CON': 1, 'INT': 1, 'WIS': 1, 'CHA': 1}
        def_traits = {}
        def_languages = ['common']
        super(Human, self).__init__(name='Human',
                                    asi=def_asi,
                                    size='medium',
                                    speed=25,
                                    languages=def_languages+languages,
                                    traits=def_traits)
    
    def _required_customization(self):
        req = [
            {
                'languages': {
                    'description': 'choose any one language',
                    'choice': 1,
                }
            }
        ]
        return req

    def _verify(self):
        # TODO try to de-dupe a lot of this proficiency stuff
        if len(self.languages) != 2:
            raise ValueError('Must input one custom language!')
        return True
