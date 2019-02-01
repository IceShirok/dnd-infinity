
from ddddd.entity import base
from ddddd.entity.base import AbilityScore, Languages, Sizes

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


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
        self.__traits = traits if traits else {}

    @property
    def traits(self):
        def_traits = {
            base.SIZE: {
                base.NAME: 'Size',
                base.DESCRIPTION: 'Your size is {}.'.format(self.size.capitalize()),
            },
        }
        return {**self.__traits, **def_traits}

    @property
    def str_movement_multiplier(self):
        return Sizes.SIZE_TO_CARRYING_CAPACITY[self.size]

    @property
    def skills(self):
        return []

    @property
    def proficiencies(self):
        return {}

    def __json__(self):
        j = {
            base.RACE: self.name,
            base.ASI: self.asi,
            base.SIZE: self.size,
            base.SPEED: self.speed,
            base.LANGUAGES: self.languages,
            base.TRAITS: self.__traits,
        }
        return j

    def verify(self):
        """
        Verify to see whether the race is properly init'd with valid values
        :return: True if valid, otherwise it'll throw an exception
        """
        required_traits = {}
        for req_k, trait_req_details in self.required().items():
            # Go through the list of traits and verify based on specifications
            if req_k not in self.traits:
                required_traits[req_k] = trait_req_details
                required_traits[req_k]['issue'] = 'Required trait {} not inputted!'.format(req_k)

            input_details = self.traits[req_k]

            choices_list_k = set(trait_req_details.keys()).intersection(set(input_details.keys())).pop()
            input_list = input_details[choices_list_k]
            if len(input_list) != trait_req_details[base.CHOICES] \
                    or not set(input_list).issubset(trait_req_details[choices_list_k]):
                required_traits[req_k] = trait_req_details
                required_traits[req_k]['issue'] = 'Required trait {} is invalid.'.format(req_k)

        return required_traits

    def required(self):
        return {}


# DWARF
class Dwarf(Race):
    def __init__(self, asi, traits):
        def_asi = {AbilityScore.CON: 2}
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
        traits = traits if traits else {}
        super(Dwarf, self).__init__(name='Dwarf',
                                    asi={**def_asi, **asi},
                                    size=Sizes.MEDIUM,
                                    speed=25,
                                    languages=[Languages.COMMON, Languages.DWARVISH],
                                    traits={**def_traits, **traits})
    
    @property
    def proficiencies(self):
        return {
            base.WEAPONS: self.traits['dwarven_combat_training'][base.WEAPON_PROFICIENCY],
            base.TOOLS: self.traits[base.TOOL_PROFICIENCY][base.TOOLS],
        }

    def required(self):
        return {
            base.TOOL_PROFICIENCY: {
                base.TOOLS: ['smiths_tools', 'brewers_kit', 'masons_tools'],
                base.CHOICES: 1,
            }
        }


class HillDwarf(Dwarf):
    def __init__(self, traits):
        def_asi = {AbilityScore.WIS: 1}
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
        def_asi = {AbilityScore.INT: 2}
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
                                    size=Sizes.SMALL,
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
        super(RockGnome, self).__init__(asi={AbilityScore.CON: 1},
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
            AbilityScore.STR: 1,
            AbilityScore.DEX: 1,
            AbilityScore.CON: 1,
            AbilityScore.INT: 1,
            AbilityScore.WIS: 1,
            AbilityScore.CHA: 1
        }
        def_traits = {}
        def_languages = [Languages.COMMON]
        super(Human, self).__init__(name='Human',
                                    asi=def_asi,
                                    size=Sizes.MEDIUM,
                                    speed=30,
                                    languages=def_languages+languages,
                                    traits=def_traits)
    
    def required(self):
        return {
            base.LANGUAGES: {
                base.LANGUAGES: Languages.LANGUAGES,
                base.CHOICES: 1,
            }
        }

    def verify(self):
        language_details = self.required()[base.LANGUAGES]
        language_list = self.languages
        if len(language_list) != language_details[base.CHOICES] \
                or not set(language_list).issubset(language_details[base.LANGUAGES]):
            raise ValueError('Required trait {} is invalid.'.format(base.LANGUAGES))
        return True
