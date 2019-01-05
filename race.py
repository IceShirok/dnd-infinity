
import json
from base import Jsonable


class Race(Jsonable):
    def __init__(self, name, asi, size, speed, languages=['common'], traits={}):
        self.name = name
        self.asi = asi
        self.size = size
        self.speed = speed
        self.languages = languages
        self.traits = traits

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
                'tool_proficiency': {
                    'tools': ['smiths_tools', 'brewers_kit', 'masons_tools'],
                    'choice': 1,
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

class HillDwarf(Dwarf):
    def __init__(self, traits):
        super(HillDwarf, self).__init__(asi={'WIS': 1},
                                            traits={
                                                'dwarven_toughness': {
                                                    'description': 'increase 1 HP per level',
                                                },
                                            })
        self.name = 'Hill Dwarf'

