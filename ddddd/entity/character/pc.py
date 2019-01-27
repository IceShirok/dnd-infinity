
import math
import json

from ddddd.entity import base
from ddddd.entity.base import AbilityScores, Skills
from ddddd.entity.character import equipment

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class PlayerBase(base.Jsonable):
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
            AbilityScores.STR: self._str,
            AbilityScores.DEX: self._dex,
            AbilityScores.CON: self._con,
            AbilityScores.INT: self._int,
            AbilityScores.WIS: self._wis,
            AbilityScores.CHA: self._cha,
        }

    def __json__(self):
        j = {
            base.NAME: self.name,
            base.BASE_ABILITY_SCORES: self.ability_scores,
            base.LEVEL: self.level,
            base.PROF_BONUS: self.proficiency_bonus,
        }
        return j

    def __str__(self):
        return json.dumps(self.__json__())

    @property
    def proficiency_bonus(self):
        # Proficiency bonus is based on a character's level.
        return math.floor((self.level + 3) / 4) + 1


class PlayerCharacter(base.Jsonable):
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
                base.SCORE: score,
                base.MODIFIER: base.modifier(score),
            }

        return ability_scores_p

    @property
    def armor_class(self):
        return 10 + self.ability_scores[AbilityScores.DEX][base.MODIFIER]

    @property
    def initiative(self):
        return self.ability_scores[AbilityScores.DEX][base.MODIFIER]

    @property
    def max_hit_points(self):
        hit_points = 0
        for c in self.classes:
            if hit_points <= 0:
                hit_points = c.hit_die + self.ability_scores[AbilityScores.CON][base.MODIFIER]
            else:
                hit_points += math.ceil(c.hit_die/2) + self.ability_scores[AbilityScores.CON][base.MODIFIER]
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
            saving_throws_p[a] = {base.MODIFIER: _ability_scores[a][base.MODIFIER]}
            saving_throws_p[a][base.IS_PROFICIENT] = False
            if a in saving_throws:
                saving_throws_p[a][base.MODIFIER] += self.proficiency_bonus
                saving_throws_p[a][base.IS_PROFICIENT] = True
        return saving_throws_p
    
    @property
    def skill_proficiencies(self):
        skill_proficiencies = (self.race.skills + self.background.skills)
        for c in self.classes:
            skill_proficiencies = skill_proficiencies + c.skills

        _ability_scores = self.ability_scores
        skill_proficiencies_p = {}
        for ability in Skills.SKILL_PROFICIENCIES_BY_ABILITY_SCORE.keys():
            for skill in Skills.SKILL_PROFICIENCIES_BY_ABILITY_SCORE[ability]:
                skill_proficiencies_p[skill] = {
                    base.ABILITY: ability,
                    base.IS_PROFICIENT: False,
                }
                skill_proficiencies_p[skill][base.MODIFIER] = _ability_scores[ability][base.MODIFIER]
                if skill in skill_proficiencies:
                    skill_proficiencies_p[skill][base.IS_PROFICIENT] = True
                    skill_proficiencies_p[skill][base.MODIFIER] += self.proficiency_bonus
        return skill_proficiencies_p
    
    @property
    def proficiencies(self):
        logger.debug('Racial proficiencies: {}'.format(self.race.proficiencies))
        logger.debug('Class proficiencies: {}'.format(self.class_proficiencies))
        logger.debug('Background proficiencies: {}'.format(self.background.proficiencies))
        p = {}
        for prof_group in [self.race.proficiencies, self.class_proficiencies, self.background.proficiencies]:
            for prof in prof_group.keys():
                if prof in p:
                    p[prof] = p[prof] + prof_group[prof]
                else:
                    p[prof] = prof_group[prof]
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
            base.RACIAL_TRAITS: self.race.traits,
            base.CLASS_FEATURES: self.class_features,
            base.BACKGROUND_FEATURES: self.background.feature,
        }

    @property
    def spellcasting(self):
        return self.classes[-1].spellcasting

    @property
    def carrying_weight(self):
        return self.worn_items.total_weight + self.backpack.total_weight

    @property
    def carrying_capacity(self):
        return self.ability_scores[AbilityScores.STR][base.SCORE] * 15 * self.race.str_movement_multiplier

    def __json__(self):
        j_classes = []
        for c in self.classes:
            j_classes.append(c.__json__())
        j = self.base.__json__()
        j[base.CLASSES] = j_classes

        if self.race:
            j[base.RACE] = self.race.__json__()
        
        if self.background:
            j[base.BACKGROUND] = self.background.__json__()
    
        return j

    def generate_character_sheet(self):
        j = {
            base.NAME: self.name,
            base.BASIC: {
                base.RACE: self.race_name,
                base.CLASS: self.class_name,
                base.LEVEL: self.level,
                base.BACKGROUND: self.background_name,
            },
            base.PROF_BONUS: self.proficiency_bonus,
            base.ABILITY_SCORES: self.ability_scores,
            base.SAVING_THROWS: self.saving_throws,
            base.SKILLS: self.skill_proficiencies,
            base.PROFICIENCIES: self.proficiencies,
            base.COMBAT: {
                base.ARMOR_CLASS: self.armor_class,
                base.INITIATIVE: self.initiative,
                base.SPEED: self.speed,
            },
            base.HIT_POINTS: {
                base.MAX_HP: self.max_hit_points,
                base.TOTAL_HIT_DICE: self.total_hit_dice,
            },
            base.TRAITS_AND_FEATURES: self.features,
            base.SPELLCASTING: self.spellcasting.__json__(),
            base.EQUIPMENT: {
                base.CARRYING_WEIGHT: self.carrying_weight,
                base.CARRYING_CAPACITY: self.carrying_capacity,
                base.WORN_ITEMS: self.worn_items.__json__(),
                base.BACKPACK: self.backpack.__json__(),
            },
        }
        return j
