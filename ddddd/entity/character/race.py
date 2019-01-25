
from ddddd.entity import ability_score, language

RACE = 'race'
SIZE = 'size'
SPEED = 'speed'
LANGUAGES = 'languages'
ASI = 'ability_score_increase'
TRAITS = 'traits'

NAME = 'name'
DESCRIPTION = 'description'
CHOICES = 'choices'

SMALL = 'small'
MEDIUM = 'medium'
SIZES = {
    SMALL,
    MEDIUM,
}

WEAPONS = 'weapons'
WEAPON_PROFICIENCY = 'weapon_proficiency'
ARMOR = 'armor'
TOOLS = 'tools'
TOOL_PROFICIENCY = 'tool_proficiency'


class Race(object):
    """
    A player character's (PC) race.
    A PC's race does not change for the most part, although
    some features may scale up with a PC's level.
    """
    def __init__(self, name, asi, size, speed, languages: list = None, traits=None):
        self.name = name
        self.asi = asi
        self.size = size
        self.speed = speed
        self.languages = languages if languages else []  # Change this for races like Kenku
        def_traits = {
            SIZE: {
                NAME: 'Size',
                DESCRIPTION: 'Your size is {}.'.format(self.size.capitalize()),
            },
        }
        self.traits = {**traits, **def_traits}
        
        self._verify()

    def __json__(self):
        j = {
                RACE: self.name,
                ASI: self.asi,
                SIZE: self.size,
                SPEED: self.speed,
                LANGUAGES: self.languages,
                TRAITS: self.traits,
            }
        return j

    def _verify(self):
        """
        Verify to see whether the race is properly init'd with valid values
        :return: True if valid, otherwise it'll throw an exception
        """
        return True

    def _required_customization(self):
        return None

    @property
    def skills(self):
        return []

    @property
    def proficiencies(self):
        return {}


# DWARF
class Dwarf(Race):
    def __init__(self, asi, traits):
        def_asi = {ability_score.CON: 2}
        def_traits = {
                'darkvision': {
                    NAME: 'Darkvision',
                    DESCRIPTION: 'Accustomed to life underground, you have superior vision in dark and dim Conditions. You can see in dim light within 60 feet of you as if it were bright light, and in Darkness as if it were dim light. You can''t discern color in Darkness, only shades of gray.',
                    'range': 60,
                },
                'dwarven_resilience': {
                    NAME: 'Dwarven Resilience',
                    DESCRIPTION: 'You have advantage on Saving Throws against poison, and you have Resistance against poison damage.',
                },
                'dwarven_combat_training': {
                    NAME: 'Dwarven Combat Training',
                    DESCRIPTION: 'You have proficiency with the Battleaxe, Handaxe, Light Hammer, and Warhammer.',
                    WEAPON_PROFICIENCY: ['battleaxe', 'handaxe', 'light_hammer', 'warhammer'],
                },
                'stonecunning': {
                    NAME: 'Stonecunning',
                    DESCRIPTION: 'Whenever you make an Intelligence (History) check related to the Origin of stonework, you are considered proficient in the History skill and add double your Proficiency Bonus to the check, instead of your normal Proficiency Bonus.',
                },
            }
        super(Dwarf, self).__init__(name='Dwarf',
                                    asi={**def_asi, **asi},
                                    size=MEDIUM,
                                    speed=25,
                                    languages=[language.COMMON, language.DWARVISH],
                                    traits={**def_traits, **traits})
    
    @property
    def proficiencies(self):
        return {
            WEAPONS: self.traits['dwarven_combat_training'][WEAPON_PROFICIENCY],
            TOOLS: self.traits[TOOL_PROFICIENCY][TOOLS],
        }

    def _required_customization(self):
        return {
                TOOL_PROFICIENCY: {
                    TOOLS: ['smiths_tools', 'brewers_kit', 'masons_tools'],
                    CHOICES: 1,
                }
            }

    def _verify(self):
        # TODO try to de-dupe a lot of this proficiency stuff
        if TOOL_PROFICIENCY not in self.traits:
            raise ValueError('Must input a tool proficiency!')
        if TOOLS not in self.traits[TOOL_PROFICIENCY] or len(self.traits[TOOL_PROFICIENCY][TOOLS]) != 1 or self.traits[TOOL_PROFICIENCY][TOOLS][0] not in ['smiths_tools', 'brewers_kit', 'masons_tools']:
            raise ValueError('Must enter a valid tool proficiency!')
        return True


class HillDwarf(Dwarf):
    def __init__(self, traits):
        def_asi = {ability_score.WIS: 1}
        def_traits = {
            'dwarven_toughness': {
                NAME: 'Dwarven Toughness',
                DESCRIPTION: 'Your hit point maximum increases by 1, and it increases by 1 every time you gain a level.',
            },
        }
        super(HillDwarf, self).__init__(asi=def_asi,
                                        traits={**def_traits, **traits})
        self.name = 'Hill Dwarf'


# GNOME

class Gnome(Race):
    def __init__(self, asi, traits):
        def_asi = {ability_score.INT: 2}
        def_traits = {
                'darkvision': {
                    NAME: 'Darkvision',
                    DESCRIPTION: 'Accustomed to life underground, you have superior vision in dark and dim Conditions. You can see in dim light within 60 feet of you as if it were bright light, and in Darkness as if it were dim light. You can''t discern color in Darkness, only shades of gray.',
                    'range': 60,
                },
                'gnome_cunning': {
                    NAME: 'Gnome Cunning',
                    DESCRIPTION: 'You have advantage on all Intelligence, Wisdom, and Charisma Saving Throws against magic.',
                },
            }
        super(Gnome, self).__init__(name='Gnome',
                                    asi={**def_asi, **asi},
                                    size=SMALL,
                                    speed=25,
                                    languages=[language.COMMON, language.GNOMISH],
                                    traits={**def_traits, **traits})


class RockGnome(Gnome):
    def __init__(self):
        traits = {
            'artificers_lore': {
                NAME: 'Artificer''s Lore',
                DESCRIPTION: 'Whenever you make an Intelligence (History) check related to Magic Items, alchemical Objects, or technological devices, you can add twice your Proficiency Bonus, instead of any Proficiency Bonus you normally apply.',
            },
            'tinker': {
                NAME: 'Tinker',
                DESCRIPTION: 'You have proficiency with artisan''s tools (tinker''s tools). ...',
            }
        }
        super(RockGnome, self).__init__(asi={ability_score.CON: 1},
                                        traits=traits)
        self.name = 'Rock Gnome'
    
    @property
    def proficiencies(self):
        return {
            TOOLS: ['tinkers_tools'],
        }


# HUMAN

class Human(Race):
    def __init__(self, languages):
        def_asi = {
            ability_score.STR: 1,
            ability_score.DEX: 1,
            ability_score.CON: 1,
            ability_score.INT: 1,
            ability_score.WIS: 1,
            ability_score.CHA: 1
        }
        def_traits = {}
        def_languages = [language.COMMON]
        super(Human, self).__init__(name='Human',
                                    asi=def_asi,
                                    size=MEDIUM,
                                    speed=30,
                                    languages=def_languages+languages,
                                    traits=def_traits)
    
    def _required_customization(self):
        return {
                LANGUAGES: {
                    LANGUAGES: language.LANGUAGES,
                    CHOICES: 1,
                }
            }

    def _verify(self):
        # TODO try to de-dupe a lot of this proficiency stuff
        if len(self.languages) != 2:
            raise ValueError('Must input one custom language!')
        if not set(self.languages).issubset(self._required_customization()[LANGUAGES][LANGUAGES]):
            raise ValueError('Must input a valid language!')
        return True
