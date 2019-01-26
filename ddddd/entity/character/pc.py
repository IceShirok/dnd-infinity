
import math
import json

from ddddd.entity import proficiency, ability_score
from ddddd.entity.character import equipment

ABILITY = 'ability'
SCORE = 'score'
MODIFIER = 'modifier'
IS_PROFICIENT = 'is_proficient'

NAME = 'name'
BASE_ABILITY_SCORES = 'base_ability_scores'
LEVEL = 'level'
PROF_BONUS = 'proficiency_bonus'

RACE = 'race'
CLASS = 'class'
CLASSES = 'classes'
BACKGROUND = 'background'

BASIC = 'basic'
ABILITY_SCORES = 'ability_scores'
SAVING_THROWS = 'saving_throws'
SKILLS = 'skills'
PROFICIENCIES = 'proficiencies'
COMBAT = 'combat'
ARMOR_CLASS = 'armor_class'
INITIATIVE = 'initiative'
SPEED = 'speed'
HIT_POINTS = 'hit_points'
MAX_HP = 'max_hp'
TOTAL_HIT_DICE = 'total_hit_dice'
TRAITS_AND_FEATURES = 'traits_and_features'
RACIAL_TRAITS = 'racial_traits'
CLASS_FEATURES = 'class_features'
BACKGROUND_FEATURES = 'background_feature'
SPELLCASTING = 'spellcasting'

EQUIPMENT = 'equipment'
WORN_ITEMS = 'worn_items'
BACKPACK = 'backpack'
CARRYING_WEIGHT = 'carrying_weight'
CARRYING_CAPACITY = 'carrying_capacity'


class PlayerBase(object):
    """
    A player character (PC) base will consist of the PC's name,
    base ability scores, and level by experience. Features that
    do not change with certain PC features (race, class, background)
    and cannot be derived by other features (i.e. proficiency bonus)
    are put in this class.
    Why level by experience and not by class? I'm thinking a little
    too far ahead, but it's because of multiclassing.
    """
    def __init__(self, name, _str, _dex, _con, _int, _wis, _cha, level=1):
        self.name = name

        self._str = _str
        self._dex = _dex
        self._con = _con
        self._int = _int
        self._wis = _wis
        self._cha = _cha

        self.level = level

    @property
    def ability_scores(self):
        """
        Return the base ability scores.
        """
        return {
            ability_score.STR: self._str,
            ability_score.DEX: self._dex,
            ability_score.CON: self._con,
            ability_score.INT: self._int,
            ability_score.WIS: self._wis,
            ability_score.CHA: self._cha,
        }

    def __json__(self):
        j = {
                NAME: self.name,
                BASE_ABILITY_SCORES: self.ability_scores,
                LEVEL: self.level,
                PROF_BONUS: self.proficiency_bonus,
            }
        return j

    def __str__(self):
        return json.dumps(self.__json__())

    @property
    def proficiency_bonus(self):
        # Proficiency bonus is based on a character's level.
        return math.floor((self.level + 3) / 4) + 1


class PlayerCharacter(object):
    """
    A player character (PC) in D&D.
    A PC consists of some base characteristics, a race, a class, and
    a background.
    """
    def __init__(self, base, race=None, classes=None, background=None, worn_items=None, backpack=None):
        self.base = base
        self.race = race
        self.classes = classes
        self.background = background
        self.worn_items = worn_items if worn_items else equipment.WornItems()
        self.backpack = backpack if backpack else equipment.Backpack()
    
    @property
    def name(self):
        return self.base.name
    
    @property
    def race_name(self):
        return self.race.name
    
    @property
    def class_name(self):
        # TODO maybe this will be aggregated to a class/level thing
        # this is more important with multiclassing so we can delay this
        return self.classes[0].name
    
    @property
    def level(self):
        return self.base.level
    
    @property
    def background_name(self):
        return self.background.name
    
    @property
    def proficiency_bonus(self):
        return self.base.proficiency_bonus
    
    @property
    def speed(self):
        return self.race.speed
        
    @property
    def size(self):
        return self.race.size

    @property
    def ability_scores(self):
        # Calculate the scores and modifiers for each ability score
        ability_scores_raw = self.base.ability_scores

        for a in self.race.asi.keys():
            ability_scores_raw[a] += self.race.asi[a]

        ability_scores_p = {}
        for a in ability_scores_raw.keys():
            score = ability_scores_raw[a]
            ability_scores_p[a] = {
                SCORE: score,
                MODIFIER: ability_score.modifier(score),
            }

        return ability_scores_p

    @property
    def armor_class(self):
        return 10 + self.ability_scores[ability_score.DEX][MODIFIER]

    @property
    def initiative(self):
        return self.ability_scores[ability_score.DEX][MODIFIER]

    @property
    def max_hit_points(self):
        hit_points = 0
        for c in self.classes:
            if hit_points <= 0:
                hit_points = c.hit_die + self.ability_scores[ability_score.CON][MODIFIER]
            else:
                hit_points += math.ceil(c.hit_die/2) + self.ability_scores[ability_score.CON][MODIFIER]
        return hit_points
    
    @property
    def total_hit_dice(self):
        # A bit more complex because of multiclassing feature
        hit_dice = {}
        for c in self.classes:
            hit_die = 'd{}'.format(c.hit_die)
            if hit_die not in hit_dice:
                hit_dice[hit_die] = 1
            else:
                hit_dice[hit_die] += 1
        return hit_dice
    
    @property
    def saving_throws(self):
        saving_throws = []
        for c in self.classes:
            saving_throws += c.saving_throws
        saving_throws_p = {}
        _ability_scores = self.ability_scores
        for a in _ability_scores.keys():
            saving_throws_p[a] = {MODIFIER: _ability_scores[a][MODIFIER]}
            saving_throws_p[a][IS_PROFICIENT] = False
            if a in saving_throws:
                saving_throws_p[a][MODIFIER] += self.proficiency_bonus
                saving_throws_p[a][IS_PROFICIENT] = True
        return saving_throws_p
    
    @property
    def skill_proficiencies(self):
        skill_proficiencies = (self.race.skills + self.background.skills)
        for c in self.classes:
            skill_proficiencies = skill_proficiencies + c.skills

        _ability_scores = self.ability_scores
        skill_proficiencies_p = {}
        for ability in proficiency.SKILL_PROFICIENCIES_BY_ABILITY_SCORE.keys():
            for skill in proficiency.SKILL_PROFICIENCIES_BY_ABILITY_SCORE[ability]:
                skill_proficiencies_p[skill] = {
                    ABILITY: ability,
                    IS_PROFICIENT: False,
                }
                skill_proficiencies_p[skill][MODIFIER] = _ability_scores[ability][MODIFIER]
                if skill in skill_proficiencies:
                    skill_proficiencies_p[skill][IS_PROFICIENT] = True
                    skill_proficiencies_p[skill][MODIFIER] += self.proficiency_bonus
        return skill_proficiencies_p
    
    @property
    def proficiencies(self):
        p = {**self.race.proficiencies, **self.class_proficiencies, **self.background.proficiencies}
        return p

    @property
    def class_proficiencies(self):
        p = {}
        for c in self.classes:
            p = {**p, **c.proficiencies}
        return p
    
    @property
    def languages(self):
        lang = (self.race.languages + self.background.languages)
        for c in self.classes:
            lang = lang + c.languages
        return lang

    @property
    def class_features(self):
        skill_features = {}
        for c in self.classes:
            skill_features = {**skill_features, **c.features}
        return skill_features

    @property
    def features(self):
        return {
            RACIAL_TRAITS: self.race.traits,
            CLASS_FEATURES: self.class_features,
            BACKGROUND_FEATURES: self.background.feature,
        }
    
    def get_spellcasting(self):
        spellcasting_p = {}
        for c in self.classes:
            if c.spellcasting:
                spellcasting_p = c.spellcasting.__json__()
        return spellcasting_p

    @property
    def carrying_weight(self):
        return self.worn_items.total_weight + self.backpack.total_weight

    @property
    def carrying_capacity(self):
        return self.ability_scores[ability_score.STR][SCORE] * 15 * self.race.str_movement_multiplier

    def __json__(self):
        j_classes = []
        for c in self.classes:
            j_classes.append(c.__json__())
        j = self.base.__json__()
        j[CLASSES] = j_classes

        if self.race:
            j[RACE] = self.race.__json__()
        
        if self.background:
            j[BACKGROUND] = self.background.__json__()
    
        return j

    def generate_character_sheet(self):
        j = {
            NAME: self.name,
            BASIC: {
                RACE: self.race_name,
                CLASS: self.class_name,
                LEVEL: self.level,
                BACKGROUND: self.background_name,
            },
            PROF_BONUS: self.proficiency_bonus,
            ABILITY_SCORES: self.ability_scores,
            SAVING_THROWS: self.saving_throws,
            SKILLS: self.skill_proficiencies,
            PROFICIENCIES: self.proficiencies,
            COMBAT: {
                ARMOR_CLASS: self.armor_class,
                INITIATIVE: self.initiative,
                SPEED: self.speed,
            },
            HIT_POINTS: {
                MAX_HP: self.max_hit_points,
                TOTAL_HIT_DICE: self.total_hit_dice,
            },
            TRAITS_AND_FEATURES: self.features,
            SPELLCASTING: self.get_spellcasting(),
            EQUIPMENT: {
                CARRYING_WEIGHT: self.carrying_weight,
                CARRYING_CAPACITY: self.carrying_capacity,
                WORN_ITEMS: self.worn_items.__json__(),
                BACKPACK: self.backpack.__json__(),
            },
        }
        return j
