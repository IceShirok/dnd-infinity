

import math

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
RACIAL_TRAITS = 'Racial Traits'
CLASS_FEATURES = 'Class Features'
BACKGROUND_FEATURES = 'Background Features'

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
WEAPON_PROFICIENCY = 'Weapon Proficiency'
TOOLS = 'tools'
TOOL_PROFICIENCY = 'Tool Proficiency'
ARMOR_PROFICIENCY = 'Armor Proficiency'
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
NUM_SPELLS_KNOWN = 'num_spells_known'
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


class AbilityScore(object):
    STR = 'STR'
    DEX = 'DEX'
    CON = 'CON'
    INT = 'INT'
    WIS = 'WIS'
    CHA = 'CHA'

    def __init__(self, name, score):
        self.name = name
        self.score = score

    @property
    def modifier(self):
        return modifier(self.score)

    def with_ability_score_increase(self, asi):
        if not isinstance(asi, AbilityScoreIncrease):
            raise ValueError('Must pass in an ability score increase!')
        if self.name != asi.ability:
            raise ValueError('Ability do not match!')
        return AbilityScore(self.name, self.score + asi.score_increase)


class AbilityScoreIncrease(object):
    def __init__(self, ability, score_increase):
        self.ability = ability
        self.score_increase = score_increase

    def combine(self, asi):
        if not isinstance(asi, AbilityScoreIncrease):
            raise ValueError('Must pass in an ability score increase!')
        if self.ability != asi.ability:
            raise ValueError('Ability do not match!')
        return AbilityScoreIncrease(self.ability, self.score_increase + asi.score_increase)


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
        AbilityScore.STR: [ATHLETICS],
        AbilityScore.DEX: [ACROBATICS, SLEIGHT_OF_HAND, STEALTH],
        AbilityScore.INT: [ARCANA, HISTORY, INVESTIGATION, NATURE, RELIGION],
        AbilityScore.WIS: [ANIMAL_HANDLING, INSIGHT, MEDICINE, PERCEPTION, SURVIVAL],
        AbilityScore.CHA: [DECEPTION, INTIMIDATION, PERFORMANCE, PERSUASION],
    }


class Languages(object):
    COMMON = 'common'
    DWARVISH = 'dwarvish'
    GNOMISH = 'gnomish'
    DRACONIC = 'draconic'
    INFERNAL = 'infernal'
    CELESTIAL = 'celestial'

    THIEVES_CANT = 'thieves cant'

    LANGUAGES = {
        COMMON,
        DWARVISH,
        GNOMISH,
        DRACONIC,
        INFERNAL,
        CELESTIAL,

        THIEVES_CANT,
    }
