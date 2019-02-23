

import math


#############################
# Common functions
#############################


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


##########################################################
# CONSTANTS TO SHARE BETWEEN MODULES
##########################################################

MODIFIER = 'modifier'
ABILITY = 'ability'
SCORE = 'score'

ABILITY_SCORES = 'ability_scores'
PROF_BONUS = 'proficiency_bonus'

BASIC = 'basic'
COMBAT = 'combat'
ARMOR_CLASS = 'armor_class'
INITIATIVE = 'initiative'
HIT_POINTS = 'hit_points'
MAX_HP = 'max_hp'
TOTAL_HIT_DICE = 'total_hit_dice'
TRAITS_AND_FEATURES = 'traits_and_features'
RACIAL_TRAITS = 'Racial Traits'
VOCATION_FEATURES = 'Class Features'
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
EXPERTISE = 'expertise'

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


#############################
# ABILITY SCORES
#############################

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


#############################
# SAVING THROWS
#############################

class SavingThrow(object):
    def __init__(self, ability_score, proficiency_bonus, is_proficient):
        self.ability_score = ability_score
        self.proficiency_bonus = proficiency_bonus
        self.is_proficient = is_proficient

    @property
    def ability(self):
        return self.ability_score.name

    @property
    def modifier(self):
        mod = modifier(self.ability_score.score)
        if self.is_proficient:
            mod += self.proficiency_bonus
        return mod


#############################
# SKILLS
#############################

class SkillProficiency(object):
    def __init__(self, name, ability_score, proficiency_bonus, is_proficient, expertise):
        self.name = name
        self.ability_score = ability_score
        self.proficiency_bonus = proficiency_bonus
        self.is_proficient = is_proficient
        self.expertise = expertise

    @property
    def ability(self):
        return self.ability_score.name

    @property
    def modifier(self):
        mod = modifier(self.ability_score.score)
        if self.is_proficient:
            mod += self.proficiency_bonus
            # You can't be an expert if you're not proficient in the skill
            if self.expertise:
                mod += self.proficiency_bonus
        return mod


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


#############################
# MISC COMMON CONSTANTS
#############################


class Languages(object):
    COMMON = 'Common'
    DWARVISH = 'Dwarvish'
    GNOMISH = 'Gnomish'
    DRACONIC = 'Draconic'
    INFERNAL = 'Infernal'
    CELESTIAL = 'Celestial'
    ELVISH = 'Elvish'
    UNDERCOMMON = 'Undercommon'

    THIEVES_CANT = "Thieves' Cant"

    LANGUAGES = {
        COMMON,
        DWARVISH,
        GNOMISH,
        DRACONIC,
        INFERNAL,
        CELESTIAL,
        ELVISH,
        UNDERCOMMON,

        THIEVES_CANT,
    }


#############################
# ENTITY BASE
#############################

class EntityBase(object):
    """
    A player character (PC) will consist of the PC's name,
    ability scores, and level by experience. Features that
    do not change with certain PC features (race, class, background)
    and cannot be derived by other features (i.e. proficiency bonus)
    are put in this class.
    Why level by experience and not by class? I'm thinking a little
    too far ahead, but it's because of multiclassing.
    """
    def __init__(self, name, str_, dex_, con_, int_, wis_, cha_, level=1):
        self.name = name

        self.str_ = AbilityScore(AbilityScore.STR, str_)
        self.dex_ = AbilityScore(AbilityScore.DEX, dex_)
        self.con_ = AbilityScore(AbilityScore.CON, con_)
        self.int_ = AbilityScore(AbilityScore.INT, int_)
        self.wis_ = AbilityScore(AbilityScore.WIS, wis_)
        self.cha_ = AbilityScore(AbilityScore.CHA, cha_)

        self.level = level

    @property
    def ability_scores(self):
        """
        Return the ability scores.
        """
        return {
            AbilityScore.STR: self.str_,
            AbilityScore.DEX: self.dex_,
            AbilityScore.CON: self.con_,
            AbilityScore.INT: self.int_,
            AbilityScore.WIS: self.wis_,
            AbilityScore.CHA: self.cha_,
        }

    @property
    def proficiency_bonus(self):
        """Proficiency bonus is  on a character's level."""
        return math.floor((self.level + 3) / 4) + 1
