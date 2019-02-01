
import math
import json

from ddddd.entity import base
from ddddd.entity.base import AbilityScore, Skills
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
            AbilityScore.STR: self._str,
            AbilityScore.DEX: self._dex,
            AbilityScore.CON: self._con,
            AbilityScore.INT: self._int,
            AbilityScore.WIS: self._wis,
            AbilityScore.CHA: self._cha,
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
        return self.classes.name
    
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

        for asi in self.classes.asi:
            for a in asi:
                ability_scores_raw[a] += asi[a]

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
        armor_obj = self.worn_items.armor
        if armor_obj:
            import inspect
            check_for_args = inspect.getfullargspec(armor_obj.armor_class)
            if check_for_args.args:
                return armor_obj.armor_class(self.ability_scores[base.AbilityScore.DEX][base.MODIFIER])
            else:
                return armor_obj.armor_class()
        return 10 + self.ability_scores[AbilityScore.DEX][base.MODIFIER]

    @property
    def initiative(self):
        return self.ability_scores[AbilityScore.DEX][base.MODIFIER]

    @property
    def max_hit_points(self):
        hit_points = 0
        hit_die = self.classes.hit_die
        for i in range(1, self.classes.level+1):
            if hit_points <= 0:
                hit_points = hit_die + self.ability_scores[AbilityScore.CON][base.MODIFIER]
            else:
                hit_points += math.ceil(hit_die/2) + self.ability_scores[AbilityScore.CON][base.MODIFIER]
        return hit_points
    
    @property
    def total_hit_dice(self):
        return {'d{}'.format(self.classes.hit_die): self.classes.level}

    @property
    def total_hit_dice_prettified(self):
        return '{}d{}'.format(self.classes.level, self.classes.hit_die)
    
    @property
    def saving_throws(self):
        saving_throws = self.classes.saving_throws
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
        skill_proficiencies = (self.race.skills + self.classes.skills + self.background.skills)

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
                    p[prof] = p[prof] + prof_group[prof].proficiencies
                else:
                    p[prof] = prof_group[prof].proficiencies
        logger.debug(p)
        return p

    @property
    def class_proficiencies(self):
        return self.classes.proficiencies
    
    @property
    def languages(self):
        langs = []
        for lang_opt in [self.race.languages, self.classes.languages, self.background.languages]:
            if lang_opt:
                langs = langs + lang_opt.languages
        return langs

    @property
    def class_features(self):
        return self.classes.features

    @property
    def features(self):
        return {
            base.RACIAL_TRAITS: self.race.traits,
            base.CLASS_FEATURES: self.class_features,
            base.BACKGROUND_FEATURES: [self.background.feature],
        }

    @property
    def spellcasting(self):
        return self.classes.spellcasting

    @property
    def carrying_weight(self):
        return self.worn_items.total_weight + self.backpack.total_weight

    @property
    def carrying_capacity(self):
        return self.ability_scores[AbilityScore.STR][base.SCORE] * 15 * self.race.str_movement_multiplier

    def calculate_weapon_bonuses(self):
        bonuses = {}
        weapons = self.worn_items.weapons
        weapon_proficiencies = self.proficiencies[base.WEAPON_PROFICIENCY]
        for weapon in weapons:
            damage_bonus = self.ability_scores[base.AbilityScore.STR][base.MODIFIER]
            attack_prof = 0
            if weapon.name in weapon_proficiencies:
                attack_prof = self.proficiency_bonus
            bonuses[weapon.name] = {
                'attack_bonus': damage_bonus + attack_prof,
                'damage': '{} + {}'.format(weapon.damage, damage_bonus),
            }
        return bonuses

    def __json__(self):
        j = self.base.__json__()

        if self.race:
            j[base.RACE] = self.race.__json__()

        if self.classes:
            j[base.CLASS] = self.classes.__json__()

        if self.background:
            j[base.BACKGROUND] = self.background.__json__()

        if self.worn_items:
            j[base.WORN_ITEMS] = self.worn_items.__json__()

        if self.backpack:
            j[base.BACKPACK] = self.backpack.__json__()
    
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
