from ddddd.entity.character import feature, base
from ddddd.entity.character.base import Languages, Sizes

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class Race(object):
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
        self.languages = languages
        self.traits = traits

    @property
    def str_movement_multiplier(self):
        return Sizes.SIZE_TO_CARRYING_CAPACITY[self.size]

    @property
    def skills(self):
        return []

    @property
    def proficiencies(self):
        prof = {}
        for p in self.traits:
            if isinstance(p, feature.ProficiencyKnown):
                prof[p.proficiency_type] = p
        return prof

    def verify(self):
        """
        Verify to see whether the race is properly init'd with valid values
        :return: True if valid, otherwise it'll throw an exception
        """
        required_traits = {}
        # for req_k, trait_req_details in self.required().items():
        #     # Go through the list of traits and verify based on specifications
        #     if req_k not in self.traits:
        #         required_traits[req_k] = trait_req_details
        #         required_traits[req_k]['issue'] = 'Required trait {} not inputted!'.format(req_k)
        #
        #     input_details = self.traits[req_k]
        #
        #     choices_list_k = set(trait_req_details.keys()).intersection(set(input_details.keys())).pop()
        #     input_list = input_details[choices_list_k]
        #     if len(input_list) != trait_req_details[base.CHOICES] \
        #             or not set(input_list).issubset(trait_req_details[choices_list_k]):
        #         required_traits[req_k] = trait_req_details
        #         required_traits[req_k]['issue'] = 'Required trait {} is invalid.'.format(req_k)

        return required_traits

    def required(self):
        return {}


#############################
# DWARF
#############################

class Dwarf(Race):
    def __init__(self, asi, traits):
        def_asi = {
            base.AbilityScore.CON: base.AbilityScoreIncrease(base.AbilityScore.CON, 2)
        }
        def_traits = [
            feature.Darkvision(range=60),
            feature.Feature(name='Dwarven Resilience',
                            description='You have advantage on Saving Throws against poison, \
                                              and you have Resistance against poison damage.'),
            feature.WeaponProficiency(name='Dwarven Combat Training',
                                      proficiencies=['battleaxe', 'handaxe',
                                                   'light_hammer', 'warhammer']),
            feature.Feature(name='Stonecunning',
                            description='Whenever you make an Intelligence (History) check related \
                                        to the Origin of stonework, you are considered proficient in the \
                                        History skill and add double your Proficiency Bonus to the check, \
                                        instead of your normal Proficiency Bonus.'),
        ]
        traits = traits if traits else {}
        super(Dwarf, self).__init__(name='Dwarf',
                                    asi={**def_asi, **asi},
                                    size=Sizes.MEDIUM,
                                    speed=25,
                                    languages=feature.LanguagesKnown(languages=[Languages.COMMON, Languages.DWARVISH]),
                                    traits=def_traits+traits)

    @property
    def base_race(self):
        return 'Dwarf'

    def required(self):
        return {
            base.TOOL_PROFICIENCY: {
                base.TOOLS: ['smiths_tools', 'brewers_kit', 'masons_tools'],
                base.CHOICES: 1,
            }
        }


class HillDwarf(Dwarf):
    def __init__(self, traits):
        def_asi = {
            base.AbilityScore.WIS: base.AbilityScoreIncrease(base.AbilityScore.WIS, 1)
        }
        def_traits = [
            feature.Toughness(name='Dwarven Toughness'),
        ]
        super(HillDwarf, self).__init__(asi=def_asi,
                                        traits=def_traits+traits)
        self.name = 'Hill Dwarf'


#############################
# GNOME
#############################

class Gnome(Race):
    def __init__(self, asi, traits):
        def_asi = {
            base.AbilityScore.INT: base.AbilityScoreIncrease(base.AbilityScore.INT, 2)
        }
        def_traits = [
            feature.Darkvision(range=60),
            feature.Feature(name='Gnome Cunning',
                            description='You have advantage on all Intelligence, Wisdom, \
                        and Charisma Saving Throws against magic.'),
        ]
        super(Gnome, self).__init__(name='Gnome',
                                    asi={**def_asi, **asi},
                                    size=Sizes.SMALL,
                                    speed=25,
                                    languages=feature.LanguagesKnown(languages=[Languages.COMMON, Languages.GNOMISH]),
                                    traits=def_traits+traits)

    @property
    def base_race(self):
        return 'Gnome'


class RockGnome(Gnome):
    def __init__(self):
        asi = {
            base.AbilityScore.CON: base.AbilityScoreIncrease(base.AbilityScore.CON, 1)
        }
        traits = [
            feature.Feature(name="Artificer's Lore",
                            description='Whenever you make an Intelligence (History) check related to Magic Items, \
                        alchemical Objects, or technological devices, you can add twice your Proficiency Bonus, \
                        instead of any Proficiency Bonus you normally apply.'),
            feature.ToolProficiency(name='Tinker',
                                    description='Using those tools, you can spend 1 hour and 10 gp worth of materials \
                                  to construct a Tiny clockwork device (AC 5, 1 hp).',
                                    proficiencies=['tinkers_tools']),
        ]
        super(RockGnome, self).__init__(asi=asi,
                                        traits=traits)
        self.name = 'Rock Gnome'


#############################
# TIEFLING
#############################

class Tiefling(Race):
    def __init__(self):
        def_asi = {
            base.AbilityScore.CHA: base.AbilityScoreIncrease(base.AbilityScore.CHA, 2),
            base.AbilityScore.INT: base.AbilityScoreIncrease(base.AbilityScore.INT, 1)
        }
        def_traits = [
            feature.Darkvision(range=60),
            feature.Feature(name='Hellish Resistance',
                            description='You have Resistance to fire damage.'),
            # TODO I guess this trait can hold spellcasting stuff?
            feature.Feature(name='Infernal Legacy',
                            description='You know the Thaumaturgy cantrip.'),
        ]
        super(Tiefling, self).__init__(name='Tiefling',
                                       asi=def_asi,
                                       size=Sizes.MEDIUM,
                                       speed=30,
                                       languages=feature.LanguagesKnown(languages=[Languages.COMMON, Languages.INFERNAL]),
                                       traits=def_traits)

    @property
    def base_race(self):
        return 'Tiefling'


#############################
# DRAGONBORN
#############################

class Dragonborn(Race):
    def __init__(self, draconic_ancestry):
        def_asi = {
            base.AbilityScore.STR: base.AbilityScoreIncrease(base.AbilityScore.STR, 2),
            base.AbilityScore.CHA: base.AbilityScoreIncrease(base.AbilityScore.CHA, 1)
        }
        super(Dragonborn, self).__init__(name=self.get_draconic_race(draconic_ancestry),
                                         asi=def_asi,
                                         size=Sizes.MEDIUM,
                                         speed=30,
                                         languages=feature.LanguagesKnown(languages=[Languages.COMMON, Languages.DRACONIC]),
                                         traits=self.get_draconic_ancestry_traits(draconic_ancestry))

    @property
    def base_race(self):
        return 'Dragonborn'

    def get_draconic_race(self, draconic_ancestry):
        if draconic_ancestry not in self._DRACONIC_ANCESTRY:
            raise ValueError('{} is not a valid draconic ancestry!')
        return '{} Dragonborn'.format(draconic_ancestry.capitalize())

    def get_draconic_ancestry_traits(self, draconic_ancestry):
        if draconic_ancestry not in self._DRACONIC_ANCESTRY:
            raise ValueError('{} is not a valid draconic ancestry!')
        ancestry_details = self._DRACONIC_ANCESTRY[draconic_ancestry]

        traits = [
            feature.Feature(name='Draconic Ancestry',
                            description='You have Draconic ancestry with a {} dragon.'.format(draconic_ancestry)),
            feature.DamageResistance(damage_type=ancestry_details['damage_type']),
            feature.Feature(name='Breath Weapon',
                            description='You can use your action to exhale destructive energy.')
        ]

        return traits

    _DRACONIC_ANCESTRY = {
        'black': {
            'damage_type': 'acid',
            'breath_weapon': '5 by 30 ft line',
            'breath_weapon_save': 'DEX',
        },
        'blue': {
            'damage_type': 'lightning',
            'breath_weapon': '5 by 30 ft line',
            'breath_weapon_save': 'DEX',
        },
        'brass': {
            'damage_type': 'fire',
            'breath_weapon': '5 by 30 ft line',
            'breath_weapon_save': 'DEX',
        },
        'bronze': {
            'damage_type': 'lightning',
            'breath_weapon': '5 by 30 ft line',
            'breath_weapon_save': 'DEX',
        },
        'copper': {
            'damage_type': 'acid',
            'breath_weapon': '5 by 30 ft line',
            'breath_weapon_save': 'DEX',
        },
        'gold': {
            'damage_type': 'fire',
            'breath_weapon': '15 ft cone',
            'breath_weapon_save': 'CON',
        },
        'green': {
            'damage_type': 'poison',
            'breath_weapon': '15 ft cone',
            'breath_weapon_save': 'CON',
        },
        'red': {
            'damage_type': 'fire',
            'breath_weapon': '15 ft cone',
            'breath_weapon_save': 'CON',
        },
        'silver': {
            'damage_type': 'cold',
            'breath_weapon': '15 ft cone',
            'breath_weapon_save': 'CON',
        },
        'white': {
            'damage_type': 'cold',
            'breath_weapon': '15 ft cone',
            'breath_weapon_save': 'CON',
        },
    }
