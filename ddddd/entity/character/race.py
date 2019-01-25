
from ddddd.entity.base import Jsonable, Requireable
from ddddd.entity import ability_scores


class Race(Jsonable, Requireable):
    """
    A player character's (PC) race.
    A PC's race does not change for the most part, although
    some features may scale up with a PC's level.
    """
    def __init__(self, name, asi, size, speed, languages=None, traits=None):
        self.name = name
        self.asi = asi
        self.size = size
        self.speed = speed
        self.languages = languages if languages else ['common']
        self.traits = traits if traits else {}
        
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

    @property
    def skills(self):
        return []

    @property
    def proficiencies(self):
        return {}


# DWARF
class Dwarf(Race):
    def __init__(self, asi, traits):
        def_asi = {ability_scores.CON: 2}
        def_traits = {
                'darkvision': {
                    'name': 'Darkvision',
                    'range': 60,
                    'description': 'Accustomed to life underground, you have superior vision in dark and dim Conditions. You can see in dim light within 60 feet of you as if it were bright light, and in Darkness as if it were dim light. You can’t discern color in Darkness, only shades of gray.',
                },
                'dwarven_resilience': {
                    'name': 'Dwarven Resilience',
                    'description': 'You have advantage on Saving Throws against poison, and you have Resistance against poison damage.',
                },
                'dwarven_combat_training': {
                    'name': 'Dwarven Combat Training',
                    'weapon_proficiency': ['battleaxe', 'handaxe', 'light_hammer', 'warhammer'],
                    'description': 'You have proficiency with the Battleaxe, Handaxe, Light Hammer, and Warhammer.',
                },
                'stonecunning': {
                    'name': 'Stonecunning',
                    'description': 'Whenever you make an Intelligence (History) check related to the Origin of stonework, you are considered proficient in the History skill and add double your Proficiency Bonus to the check, instead of your normal Proficiency Bonus.',
                },
            }
        super(Dwarf, self).__init__(name='Dwarf',
                                    asi={**def_asi, **asi},
                                    size='medium',
                                    speed=25,
                                    languages=['common', 'dwarvish'],
                                    traits={**def_traits, **traits})
    
    @property
    def skills(self):
        return []
    
    @property
    def proficiencies(self):
        p = {
            'weapons': self.traits['dwarven_combat_training']['weapon_proficiency'],
            'tools': self.traits['tool_proficiency']['tools'],
        }
        return p

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
        if 'tools' not in self.traits['tool_proficiency'] or len(self.traits['tool_proficiency']['tools']) != 1 or self.traits['tool_proficiency']['tools'][0] not in ['smiths_tools', 'brewers_kit', 'masons_tools']:
            raise ValueError('Must enter a valid tool proficiency!')
        return True


class HillDwarf(Dwarf):
    def __init__(self, traits):
        def_asi = {ability_scores.WIS: 1}
        def_traits = {
            'dwarven_toughness': {
                'name': 'Dwarven Toughness',
                'description': 'Your hit point maximum increases by 1, and it increases by 1 every time you gain a level.',
            },
        }
        super(HillDwarf, self).__init__(asi=def_asi,
                                        traits={**def_traits, **traits})
        self.name = 'Hill Dwarf'


# GNOME

class Gnome(Race):
    def __init__(self, asi, traits):
        def_asi = {ability_scores.INT: 2}
        def_traits = {
                'darkvision': {
                    'name': 'Darkvision',
                    'range': 60,
                    'description': 'Accustomed to life underground, you have superior vision in dark and dim Conditions. You can see in dim light within 60 feet of you as if it were bright light, and in Darkness as if it were dim light. You can’t discern color in Darkness, only shades of gray.',
                },
                'gnome_cunning': {
                    'name': 'Gnome Cunning',
                    'description': 'You have advantage on all Intelligence, Wisdom, and Charisma Saving Throws against magic.',
                },
            }
        super(Gnome, self).__init__(name='Gnome',
                                    asi={**def_asi, **asi},
                                    size='small',
                                    speed=25,
                                    languages=['common', 'gnomish'],
                                    traits={**def_traits, **traits})

    @property
    def skills(self):
        return []
    
    @property
    def proficiencies(self):
        p = {}
        return p


class RockGnome(Gnome):
    def __init__(self):
        traits = {
            'artificers_lore': {
                'name': 'Artificer''s Lore',
                'description': 'Whenever you make an Intelligence (History) check related to Magic Items, alchemical Objects, or technological devices, you can add twice your Proficiency Bonus, instead of any Proficiency Bonus you normally apply.',
            },
            'tinker': {
                'name': 'Tinker',
                'description': 'You have proficiency with artisan’s tools (tinker’s tools). ...',
            }
        }
        super(RockGnome, self).__init__(asi={ability_scores.CON: 1},
                                        traits=traits)
        self.name = 'Rock Gnome'
    
    @property
    def proficiencies(self):
        p = {
            'tools': ['tinkers_tools'],
        }
        return p


# HUMAN

class Human(Race):
    def __init__(self, languages):
        def_asi = {
            ability_scores.STR: 1,
            ability_scores.DEX: 1,
            ability_scores.CON: 1,
            ability_scores.INT: 1,
            ability_scores.WIS: 1,
            ability_scores.CHA: 1
        }
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

    @property
    def skills(self):
        return []
    
    @property
    def proficiencies(self):
        p = {}
        return p
