import json
import abc
import math


class Jsonable(abc.ABC):
    """
    Create an interface to force objects to implement a JSON method
    for debugging purposes
    """
    @abc.abstractmethod
    def __json__(self):
        pass

    def __str__(self):
        return json.dumps(self.__json__())


"""
Common functions
"""


def modifier(score):
    # Calculates the ability modifier
    return math.floor((score-10)/2)


def prettify_modifier(mod):
    # Function used to add a + to positive score, - to negative score,
    # or do nothing to a 0. Used for visual purposes.
    if mod > 0:
        return '+{}'.format(mod)
    else:
        return str(mod)


# Basic constants
MODIFIER = 'modifier'
ABILITY = 'ability'
SCORE = 'score'

BASE_ABILITY_SCORES = 'base_ability_scores'
PROF_BONUS = 'proficiency_bonus'

BASIC = 'basic'
ABILITY_SCORES = 'ability_scores'
COMBAT = 'combat'
ARMOR_CLASS = 'armor_class'
INITIATIVE = 'initiative'
HIT_POINTS = 'hit_points'
MAX_HP = 'max_hp'
TOTAL_HIT_DICE = 'total_hit_dice'
TRAITS_AND_FEATURES = 'traits_and_features'
RACIAL_TRAITS = 'racial_traits'
CLASS_FEATURES = 'class_features'
BACKGROUND_FEATURES = 'background_feature'

# Race-related constants
RACE = 'race'
SIZE = 'size'
SPEED = 'speed'
ASI = 'ability_score_increase'
TRAITS = 'traits'

# Used for validation
NAME = 'name'
DESCRIPTION = 'description'
CHOICES = 'choices'

# Proficiency-related constants
WEAPON_PROFICIENCY = 'weapon_proficiency'
TOOLS = 'tools'
TOOL_PROFICIENCY = 'tool_proficiency'
LANGUAGES = 'languages'
SKILL_PROF = 'skill_proficiency'
SKILL_PROFS = 'skill_proficiencies'
IS_PROFICIENT = 'is_proficient'

# Class-related constants
CLASS = 'class'
CLASSES = 'classes'
LEVEL = 'level'
HIT_DIE = 'hit_die'
PROFICIENCIES = 'proficiencies'
SAVING_THROWS = 'saving_throws'
SKILLS = 'skills'
FEATURES = 'features'
SPELLCASTING = 'spellcasting'

# Background-related constants
BACKGROUND = 'background'

# Equipment-related constants
EQUIPMENT = 'equipment'
WORN_ITEMS = 'worn_items'
BACKPACK = 'backpack'
CARRYING_WEIGHT = 'carrying_weight'
CARRYING_CAPACITY = 'carrying_capacity'

WEAPONS = 'weapons'
ARMOR = 'armor'
TOTAL_WEIGHT = 'total_weight'
TOTAL_ITEM_WORTH = 'total_item_worth'
ITEMS = 'items'
MONEY = 'money'
COPPER_PIECES = 'CP'
SILVER_PIECES = 'SP'
GOLD_PIECES = 'GP'
PLATNIUM_PIECES = 'PP'
PRICE = 'price'
WEIGHT = 'weight'
QUANTITY = 'quantity'
DAMAGE = 'damage'
PROPERTIES = 'properties'
STRENGTH_PREREQ = 'strength'
STEALTH_PENALTY = 'stealth'

# Spellcasting-related constants
SPELL = 'spell'
SPELLCASTING_ABILITY = 'spellcasting_ability'
LIST_SPELLS_KNOWN = 'list_spells_known'
SPELL_SLOTS = 'spell_slots'
RANGE = 'range'


class SpellTypes(object):
    CANTRIPS = 'cantrips'
    FIRST = '1st'
    SECOND = '2nd'
    THIRD = '3rd'
    FOURTH = '4th'
    FIFTH = '5th'
    SIXTH = '6th'
    SEVENTH = '7th'
    EIGHTH = '8th'
    NINTH = '9th'


class AbilityScores(object):
    STR = 'STR'
    DEX = 'DEX'
    CON = 'CON'
    INT = 'INT'
    WIS = 'WIS'
    CHA = 'CHA'


class Sizes(object):
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


class Skills(object):
    ATHLETICS = 'Athletics'

    ACROBATICS = 'Acrobatics'
    SLEIGHT_OF_HAND = 'Sleight of Hand'
    STEALTH = 'Stealth'

    ARCANA = 'Arcana'
    HISTORY = 'History'
    INVESTIGATION = 'Investigation'
    NATURE = 'Nature'
    RELIGION = 'Religion'

    ANIMAL_HANDLING = 'Animal Handling'
    INSIGHT = 'Insight'
    MEDICINE = 'Medicine'
    PERCEPTION = 'Perception'
    SURVIVAL = 'Survival'

    DECEPTION = 'Deception'
    INTIMIDATION = 'Intimidation'
    PERFORMANCE = 'Performance'
    PERSUASION = 'Persuasion'

    SKILL_PROFICIENCIES_BY_ABILITY_SCORE = {
        AbilityScores.STR: [ATHLETICS],
        AbilityScores.DEX: [ACROBATICS, SLEIGHT_OF_HAND, STEALTH],
        AbilityScores.INT: [ARCANA, HISTORY, INVESTIGATION, NATURE, RELIGION],
        AbilityScores.WIS: [ANIMAL_HANDLING, INSIGHT, MEDICINE, PERCEPTION, SURVIVAL],
        AbilityScores.CHA: [DECEPTION, INTIMIDATION, PERFORMANCE, PERSUASION],
    }


class Languages(object):
    COMMON = 'common'
    DWARVISH = 'dwarvish'
    GNOMISH = 'gnomish'
    DRACONIC = 'draconic'

    LANGUAGES = {
        COMMON,
        DWARVISH,
        GNOMISH,
        DRACONIC,
    }