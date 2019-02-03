
import math

from ddddd.entity import base
from ddddd.entity.base import AbilityScore, Skills
from ddddd.entity.character import spells, trait
from ddddd.items import items, weapons

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


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
    def __init__(self, name, str_, dex_, con_, int_, wis_, cha_, level=1):
        self.name = name

        self.str_ = base.AbilityScore(base.AbilityScore.STR, str_)
        self.dex_ = base.AbilityScore(base.AbilityScore.DEX, dex_)
        self.con_ = base.AbilityScore(base.AbilityScore.CON, con_)
        self.int_ = base.AbilityScore(base.AbilityScore.INT, int_)
        self.wis_ = base.AbilityScore(base.AbilityScore.WIS, wis_)
        self.cha_ = base.AbilityScore(base.AbilityScore.CHA, cha_)

        self.level = level

    @property
    def base_ability_scores(self):
        """
        Return the base ability scores.
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
        """Proficiency bonus is based on a character's level."""
        return math.floor((self.level + 3) / 4) + 1


class PlayerCharacter(object):
    """
    A player character (PC) in D&D.
    A PC consists of some base characteristics, a race, a class, and
    a background.
    """
    def __init__(self, base, race=None, vocation=None, background=None, worn_items=None, backpack=None):
        self.base = base
        self.race = race
        self.vocation = vocation
        self.background = background
        self.worn_items = worn_items if worn_items else items.WornItems()
        self.backpack = backpack if backpack else items.Backpack()

    #########################
    # BASIC PROPERTIES
    #########################

    @property
    def name(self):
        """Return the PC's name"""
        return self.base.name
    
    @property
    def race_name(self):
        """Return the PC's race, by subrace."""
        return self.race.name

    @property
    def base_race_name(self):
        """Return the PC's race, by base race."""
        return self.race.base_race
    
    @property
    def vocation_name(self):
        """Return the PC's vocation."""
        return self.vocation.name
    
    @property
    def level(self):
        """Return the PC's character level. This is different from vocation level."""
        return self.base.level
    
    @property
    def background_name(self):
        """Return the PC's background."""
        return self.background.name
    
    @property
    def proficiency_bonus(self):
        """Return the PC's proficiency bonus."""
        return self.base.proficiency_bonus
    
    @property
    def speed(self):
        """Return the PC's speed, by feet."""
        return self.race.speed
        
    @property
    def size(self):
        """Return the PC's character size."""
        return self.race.size

    @property
    def ability_scores(self):
        """Calculate the final ability scores after aggregating all features that can affect ability score."""
        # Calculate the scores and modifiers for each ability score
        ability_scores_agg = self.base.base_ability_scores

        race_asi = self.race.asi
        for ability in race_asi.keys():
            ability_scores_agg[ability] = ability_scores_agg[ability].with_ability_score_increase(race_asi[ability])

        vocation_asi = self.vocation.asi
        for ability in vocation_asi:
            ability_scores_agg[ability] = ability_scores_agg[ability].with_ability_score_increase(vocation_asi[ability])

        return ability_scores_agg

    @property
    def armor_class(self):
        """Calculate armor class based on armor and other features."""
        armor_obj = self.worn_items.armor
        if armor_obj:
            import inspect
            check_for_args = inspect.getfullargspec(armor_obj.armor_class)
            if check_for_args.args:
                return armor_obj.armor_class(self.ability_scores[base.AbilityScore.DEX].modifier)
            else:
                return armor_obj.armor_class()
        return 10 + self.ability_scores[AbilityScore.DEX].modifier

    @property
    def initiative(self):
        """Calculate initiative based on DEX modifier and a few traits."""
        return self.ability_scores[AbilityScore.DEX].modifier

    #########################
    # HIT POINTS
    #########################

    @property
    def max_hit_points(self):
        """
        Calculate max HP based on class hit die, CON modifier, and a few features.
        :return: the max HP for the PC
        """
        hit_points = 0
        hit_die = self.vocation.hit_die
        con_modifier = self.ability_scores[AbilityScore.CON].modifier
        toughness = len(list(filter(lambda exp: isinstance(exp, trait.Toughness), self.race.traits)))

        for _ in range(0, self.vocation.level):
            if hit_points <= 0:
                hit_points = hit_die + con_modifier + toughness
            else:
                hit_points += math.ceil(hit_die/2) + con_modifier + toughness
        return hit_points
    
    @property
    def total_hit_dice(self):
        """Calculate total hit dice, based on class level and hit dice."""
        return {'d{}'.format(self.vocation.hit_die): self.vocation.level}

    @property
    def total_hit_dice_prettified(self):
        """A more prettifed verison of total hit dice."""
        return '{}d{}'.format(self.vocation.level, self.vocation.hit_die)

    #########################
    # PROFICIENCIES
    #########################

    @property
    def saving_throws(self):
        """Calculate the PC's saving throws."""
        saving_throws = self.vocation.saving_throws
        saving_throws_p = {}
        _ability_scores = self.ability_scores
        for a in _ability_scores.keys():
            saving_throws_p[a] = {base.MODIFIER: _ability_scores[a].modifier}
            saving_throws_p[a][base.IS_PROFICIENT] = False
            if a in saving_throws:
                saving_throws_p[a][base.MODIFIER] += self.proficiency_bonus
                saving_throws_p[a][base.IS_PROFICIENT] = True
        return saving_throws_p

    @property
    def skills_by_ability(self):
        """Calculates the PC's skill modifiers, and groups the skills by ability."""
        skill_proficiencies = (self.race.skills + self.vocation.skills + self.background.skills)
        expertise = list(filter(lambda exp: isinstance(exp, trait.Expertise), self.vocation.features))

        _ability_scores = self.ability_scores
        skill_proficiencies_p = {}
        for ability in Skills.SKILL_PROFICIENCIES_BY_ABILITY_SCORE.keys():
            skill_proficiencies_p[ability] = {}
            for skill in Skills.SKILL_PROFICIENCIES_BY_ABILITY_SCORE[ability]:
                skill_proficiencies_p[ability][skill] = {
                    base.ABILITY: ability,
                    base.IS_PROFICIENT: False,
                    base.EXPERTISE: False,
                }
                skill_proficiencies_p[ability][skill][base.MODIFIER] = _ability_scores[ability].modifier
                if skill in skill_proficiencies:
                    skill_proficiencies_p[ability][skill][base.IS_PROFICIENT] = True
                    skill_proficiencies_p[ability][skill][base.MODIFIER] += self.proficiency_bonus
                    for e in expertise:
                        if skill in e.skills:
                            skill_proficiencies_p[ability][skill][base.EXPERTISE] = True
                            skill_proficiencies_p[ability][skill][base.MODIFIER] += self.proficiency_bonus
        return skill_proficiencies_p
    
    @property
    def proficiencies(self):
        """Aggregate proficiencies that the PC has learned."""
        p = {
            base.WEAPON_PROFICIENCY: [],
            base.ARMOR_PROFICIENCY: [],
            base.TOOL_PROFICIENCY: [],
            base.LANGUAGES: [],
        }
        for prof_group in [self.race.proficiencies, self.vocation.proficiencies, self.background.proficiencies]:
            for prof in prof_group.keys():
                if prof not in p:
                    p[prof] = []
                p[prof] = p[prof] + prof_group[prof].proficiencies
        p[base.LANGUAGES] = self.languages

        # Weapon proficiencies are a bit strange because there are weapon categories
        # and specific weapon proficiencies.
        p[base.WEAPON_PROFICIENCY] = weapons.get_aggregated_weapon_proficiencies(p[base.WEAPON_PROFICIENCY])
        return p
    
    @property
    def languages(self):
        """Aggregate languages that the PC knows."""
        langs = []
        for lang_opt in [self.race.languages, self.vocation.languages, self.background.languages]:
            if lang_opt:
                langs = langs + lang_opt.languages
        return langs

    @property
    def racial_features(self):
        """Returns all features from race"""
        return self.race.traits

    @property
    def vocation_features(self):
        """Returns all features from the vocation"""
        return self.vocation.features

    @property
    def background_feature(self):
        """Currently background only provides one feature."""
        return [self.background.feature]

    @property
    def features(self):
        """Aggregates all features that the PC possesses."""
        return {
            base.RACIAL_TRAITS: self.racial_features,
            base.VOCATION_FEATURES: self.vocation_features,
            base.BACKGROUND_FEATURES: [self.background_feature],
        }

    #########################
    # SPELLCASTING
    #########################

    @property
    def spellcasting(self):
        """Retrieve a PC's spellcasting ability."""
        return self.vocation.spellcasting

    @property
    def cantrips(self):
        """Retrieve cantrips that the PC knows."""
        if self.spellcasting:
            return self.spellcasting.cantrips
        return None

    def calculate_damage_cantrips(self):
        """Get a list of damaging cantrips, treated like weapons."""
        damage_cantrips = list(filter(lambda c: isinstance(c, spells.DamageCantrip), self.cantrips))
        bonuses = {}
        for cantrip in damage_cantrips:
            bonuses[cantrip.name] = {
                'cantrip': cantrip,
                'attack_bonus': cantrip.attack_bonus_calc(self.spell_attack_bonus, self.spell_save_dc),
                'damage': cantrip.damage_calc(self.level),
            }
        return bonuses

    @property
    def casting_spells(self):
        """Retrieve a PC's spells (spells that require spell slots)."""
        if self.spellcasting:
            spell_by_level = {}
            list_spells = self.spellcasting.casting_spells
            for spell in list_spells:
                if spell.level not in spell_by_level:
                    spell_by_level[spell.level] = []
                spell_by_level[spell.level].append(spell)
            return spell_by_level
        return None

    @property
    def spell_attack_bonus(self):
        """Calculate a PC's spell attack bonus, if the PC can cast spells."""
        if self.spellcasting:
            return self.spellcasting.spell_attack_bonus(self.ability_scores, self.proficiency_bonus)
        return None

    @property
    def spell_save_dc(self):
        """Calculate a PC's spell save DC, if the PC can cast spells."""
        if self.spellcasting:
            return self.spellcasting.spell_save_dc(self.ability_scores, self.proficiency_bonus)
        return None

    #########################
    # EQUIPMENT
    #########################

    @property
    def carrying_weight(self):
        """Calculate the total weight of all items that PC is currently carrying."""
        return self.worn_items.total_weight + self.backpack.total_weight

    @property
    def carrying_capacity(self):
        """Calculate the maximum amount of weight the PC can carry."""
        return self.ability_scores[AbilityScore.STR].score * 15 * self.race.str_movement_multiplier

    def calculate_weapon_bonuses(self):
        """Calculate weapon bonuses."""
        bonuses = {}
        weapons = self.worn_items.weapons
        weapon_proficiencies = self.proficiencies[base.WEAPON_PROFICIENCY] if base.WEAPON_PROFICIENCY in self.proficiencies else []
        for weapon in weapons:
            str_mod = (base.AbilityScore.STR, self.ability_scores[base.AbilityScore.STR].modifier)
            dex_mod = (base.AbilityScore.DEX, self.ability_scores[base.AbilityScore.DEX].modifier)

            attack_mod = str_mod
            # TODO make this more elegant
            for w_prop in weapon.properties:
                w_prop = w_prop.lower()
                if 'ammunition' in w_prop:  # Weapon is ranged only
                    attack_mod = dex_mod
                elif 'finesse' in w_prop:  # Weapon is finesse
                    attack_mod = dex_mod if dex_mod[1] > str_mod[1] else str_mod

            attack_type, damage_bonus = attack_mod
            attack_prof = 0
            if weapon.category in weapon_proficiencies or weapon.name in weapon_proficiencies:
                attack_prof = self.proficiency_bonus
            bonuses[weapon.name] = {
                'weapon': weapon,
                'attack_bonus': damage_bonus + attack_prof,
                'attack_type': attack_type,
                'damage': '{} + {}'.format(weapon.damage, damage_bonus),
            }
        return bonuses
