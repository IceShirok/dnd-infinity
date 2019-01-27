
from ddddd.entity import base
from ddddd.entity.base import AbilityScores, Languages

TINY = 'tiny'
SMALL = 'small'
MEDIUM = 'medium'
LARGE = 'large'
HUGE = 'huge'
GARGANTUAN = 'gargantuan'
SIZE_TO_CARRYING_CAPACITY = {
    TINY: 0.5,
    SMALL: 1,
    MEDIUM: 1,
    LARGE: 2,
    HUGE: 4,
    GARGANTUAN: 8,
}


class Race(base.Jsonable):
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
            base.SIZE: {
                base.NAME: 'Size',
                base.DESCRIPTION: 'Your size is {}.'.format(self.size.capitalize()),
            },
        }
        self.traits = {**traits, **def_traits}
        
        self._verify()

    @property
    def str_movement_multiplier(self):
        return SIZE_TO_CARRYING_CAPACITY[self.size]

    def __json__(self):
        j = {
            base.RACE: self.name,
            base.ASI: self.asi,
            base.SIZE: self.size,
            base.SPEED: self.speed,
            base.LANGUAGES: self.languages,
            base.TRAITS: self.traits,
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
        def_asi = {AbilityScores.CON: 2}
        def_traits = {
                'darkvision': {
                    base.NAME: 'Darkvision',
                    base.DESCRIPTION: 'Accustomed to life underground, you have superior vision in dark and dim Conditions. You can see in dim light within 60 feet of you as if it were bright light, and in Darkness as if it were dim light. You can''t discern color in Darkness, only shades of gray.',
                    base.RANGE: 60,
                },
                'dwarven_resilience': {
                    base.NAME: 'Dwarven Resilience',
                    base.DESCRIPTION: 'You have advantage on Saving Throws against poison, and you have Resistance against poison damage.',
                },
                'dwarven_combat_training': {
                    base.NAME: 'Dwarven Combat Training',
                    base.DESCRIPTION: 'You have proficiency with the Battleaxe, Handaxe, Light Hammer, and Warhammer.',
                    base.WEAPON_PROFICIENCY: ['battleaxe', 'handaxe', 'light_hammer', 'warhammer'],
                },
                'stonecunning': {
                    base.NAME: 'Stonecunning',
                    base.DESCRIPTION: 'Whenever you make an Intelligence (History) check related to the Origin of stonework, you are considered proficient in the History skill and add double your Proficiency Bonus to the check, instead of your normal Proficiency Bonus.',
                },
            }
        super(Dwarf, self).__init__(name='Dwarf',
                                    asi={**def_asi, **asi},
                                    size=MEDIUM,
                                    speed=25,
                                    languages=[Languages.COMMON, Languages.DWARVISH],
                                    traits={**def_traits, **traits})
    
    @property
    def proficiencies(self):
        return {
            base.WEAPONS: self.traits['dwarven_combat_training'][base.WEAPON_PROFICIENCY],
            base.TOOLS: self.traits[base.TOOL_PROFICIENCY][base.TOOLS],
        }

    def _required_customization(self):
        return {
            base.TOOL_PROFICIENCY: {
                base.TOOLS: ['smiths_tools', 'brewers_kit', 'masons_tools'],
                base.CHOICES: 1,
            }
        }

    def _verify(self):
        # TODO try to de-dupe a lot of this proficiency stuff
        if base.TOOL_PROFICIENCY not in self.traits:
            raise ValueError('Must input a tool proficiency!')
        if base.TOOLS not in self.traits[base.TOOL_PROFICIENCY] \
                or len(self.traits[base.TOOL_PROFICIENCY][base.TOOLS]) != 1 \
                or self.traits[base.TOOL_PROFICIENCY][base.TOOLS][0] not in ['smiths_tools', 'brewers_kit', 'masons_tools']:
            raise ValueError('Must enter a valid tool proficiency!')
        return True


class HillDwarf(Dwarf):
    def __init__(self, traits):
        def_asi = {AbilityScores.WIS: 1}
        def_traits = {
            'dwarven_toughness': {
                base.NAME: 'Dwarven Toughness',
                base.DESCRIPTION: 'Your hit point maximum increases by 1, and it increases by 1 every time you gain a level.',
            },
        }
        super(HillDwarf, self).__init__(asi=def_asi,
                                        traits={**def_traits, **traits})
        self.name = 'Hill Dwarf'


# GNOME

class Gnome(Race):
    def __init__(self, asi, traits):
        def_asi = {AbilityScores.INT: 2}
        def_traits = {
                'darkvision': {
                    base.NAME: 'Darkvision',
                    base.DESCRIPTION: 'Accustomed to life underground, you have superior vision in dark and dim Conditions. You can see in dim light within 60 feet of you as if it were bright light, and in Darkness as if it were dim light. You can''t discern color in Darkness, only shades of gray.',
                    base.RANGE: 60,
                },
                'gnome_cunning': {
                    base.NAME: 'Gnome Cunning',
                    base.DESCRIPTION: 'You have advantage on all Intelligence, Wisdom, and Charisma Saving Throws against magic.',
                },
            }
        super(Gnome, self).__init__(name='Gnome',
                                    asi={**def_asi, **asi},
                                    size=SMALL,
                                    speed=25,
                                    languages=[Languages.COMMON, Languages.GNOMISH],
                                    traits={**def_traits, **traits})


class RockGnome(Gnome):
    def __init__(self):
        traits = {
            'artificers_lore': {
                base.NAME: 'Artificer''s Lore',
                base.DESCRIPTION: 'Whenever you make an Intelligence (History) check related to Magic Items, alchemical Objects, or technological devices, you can add twice your Proficiency Bonus, instead of any Proficiency Bonus you normally apply.',
            },
            'tinker': {
                base.NAME: 'Tinker',
                base.DESCRIPTION: 'You have proficiency with artisan''s tools (tinker''s tools). ...',
            }
        }
        super(RockGnome, self).__init__(asi={AbilityScores.CON: 1},
                                        traits=traits)
        self.name = 'Rock Gnome'
    
    @property
    def proficiencies(self):
        return {
            base.TOOLS: ['tinkers_tools'],
        }


# HUMAN

class Human(Race):
    def __init__(self, languages):
        def_asi = {
            AbilityScores.STR: 1,
            AbilityScores.DEX: 1,
            AbilityScores.CON: 1,
            AbilityScores.INT: 1,
            AbilityScores.WIS: 1,
            AbilityScores.CHA: 1
        }
        def_traits = {}
        def_languages = [Languages.COMMON]
        super(Human, self).__init__(name='Human',
                                    asi=def_asi,
                                    size=MEDIUM,
                                    speed=30,
                                    languages=def_languages+languages,
                                    traits=def_traits)
    
    def _required_customization(self):
        return {
            base.LANGUAGES: {
                base.LANGUAGES: Languages.LANGUAGES,
                base.CHOICES: 1,
            }
        }

    def _verify(self):
        # TODO try to de-dupe a lot of this proficiency stuff
        if len(self.languages) != 2:
            raise ValueError('Must input one custom language!')
        if not set(self.languages).issubset(self._required_customization()[base.LANGUAGES][base.LANGUAGES]):
            raise ValueError('Must input a valid language!')
        return True
