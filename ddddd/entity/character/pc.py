
import math

from ddddd.entity.character.base import AbilityScore, Skills
from ddddd.entity.character import spells, feature, base
from ddddd.items import items, weapons

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class PlayerCharacter(object):
    """
    A player character (PC) in D&D.
    A PC consists of some base characteristics, a race, a class, and
    a background.
    """
    def __init__(self, base_, race=None, vocation=None, background=None, worn_items=None, backpack=None):
        self.base_ = base_
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
        return self.base_.name
    
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
        return self.base_.level
    
    @property
    def background_name(self):
        """Return the PC's background."""
        return self.background.name
    
    @property
    def proficiency_bonus(self):
        """Return the PC's proficiency bonus."""
        return self.base_.proficiency_bonus
    
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
        ability_scores_agg = self.base_.ability_scores

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
        Note that the average hit die must be (1 + max_hd)/2 because of dice stuff.
        :return: the max HP for the PC
        """
        hit_points = 0
        hit_die = self.vocation.hit_die
        con_modifier = self.ability_scores[AbilityScore.CON].modifier
        toughness = len(list(filter(lambda exp: isinstance(exp, feature.Toughness), self.race.traits)))

        for _ in range(0, self.vocation.level):
            if hit_points <= 0:
                hit_points = hit_die + con_modifier + toughness
            else:
                hit_points += math.ceil((1+hit_die)/2) + con_modifier + toughness
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
            saving_throws_p[a] = base.SavingThrow(_ability_scores[a],
                                                  self.proficiency_bonus,
                                                  is_proficient=False)
            if a in saving_throws:
                saving_throws_p[a].is_proficient = True
        return saving_throws_p

    @property
    def skills_by_ability(self):
        """Calculates the PC's skill modifiers, and groups the skills by ability."""
        skill_proficiencies = (self.race.skills + self.vocation.skills + self.background.skills)
        expertise = list(filter(lambda exp: isinstance(exp, feature.Expertise), self.vocation_features))

        _ability_scores = self.ability_scores
        skill_proficiencies_p = {}
        for ability in Skills.SKILL_PROFICIENCIES_BY_ABILITY_SCORE.keys():
            skill_proficiencies_p[ability] = {}
            for skill in Skills.SKILL_PROFICIENCIES_BY_ABILITY_SCORE[ability]:
                skill_proficiencies_p[ability][skill] = base.SkillProficiency(name=skill,
                                                                              ability_score=_ability_scores[ability],
                                                                              proficiency_bonus=self.proficiency_bonus,
                                                                              is_proficient=False,
                                                                              expertise=False)
                if skill in skill_proficiencies:
                    skill_proficiencies_p[ability][skill].is_proficient = True
                    for e in expertise:
                        if skill in e.skills:
                            skill_proficiencies_p[ability][skill].expertise = True
        return skill_proficiencies_p
    
    @property
    def proficiencies(self):
        """Aggregate proficiencies that the PC has learned."""
        p = {
            base.WEAPON_PROFICIENCY: [],
            base.ARMOR_PROFICIENCY: [],
            base.TOOL_PROFICIENCY: [],
        }
        for prof_group in [self.race.proficiencies, self.vocation.proficiencies, self.background.proficiencies]:
            for prof in prof_group.keys():
                if prof not in p:
                    p[prof] = []
                p[prof] = p[prof] + prof_group[prof].proficiencies

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

    #########################
    # FEATURES & TRAITS
    #########################

    @property
    def feats(self):
        """Returns all features from race"""
        return self.vocation.feats

    @property
    def racial_traits(self):
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
            base.RACIAL_TRAITS: self.racial_traits,
            base.VOCATION_FEATURES: self.vocation_features,
            base.BACKGROUND_FEATURES: self.background_feature,
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
        bonuses = {}
        if not self.spellcasting or not self.cantrips:
            return bonuses

        damage_cantrips = list(filter(lambda c: isinstance(c, spells.DamageCantrip), self.cantrips))

        vocation_bonuses = list(filter(lambda f: isinstance(f, feature.EnhanceDamage), self.vocation_features))

        for cantrip in damage_cantrips:
            total_damage = cantrip.damage_calc(self.level)
            for bonus in vocation_bonuses:
                if bonus.qualifies(cantrip):
                    total_damage = '{} + {}'.format(total_damage, bonus.get_bonus(ability_scores=self.ability_scores))

            bonuses[cantrip.name] = {
                'cantrip': cantrip,
                'attack_bonus': cantrip.attack_bonus_calc(self.spell_attack_bonus, self.spell_save_dc),
                'damage': total_damage,
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

    @property
    def total_equipment_worth(self):
        """Calculate the total worth of the backpack's contents."""
        return self.worn_items.total_item_worth

    @property
    def total_backpack_worth(self):
        """Calculate the total worth of the backpack's contents."""
        return self.backpack.total_item_worth

    def calculate_weapon_bonuses(self):
        """Calculate weapon bonuses."""
        bonuses = {}
        weapons_ = self.worn_items.weapons
        weapon_proficiencies = self.proficiencies[base.WEAPON_PROFICIENCY] if base.WEAPON_PROFICIENCY in self.proficiencies else []
        vocation_bonuses = list(filter(lambda f: isinstance(f, feature.EnhanceDamage), self.vocation_features))

        for weapon in weapons_:
            attack_type, damage_bonus = weapons.determine_attack_bonus_type(weapon, self.ability_scores)
            attack_bonus = damage_bonus
            if weapons.is_proficient(weapon, weapon_proficiencies):
                attack_bonus += self.proficiency_bonus

            weapon_damage_list = [str(weapon.damage)]
            if damage_bonus:  # only add damage bonus if it's not zero
                weapon_damage_list.append(str(damage_bonus))

            for bonus in vocation_bonuses:
                if bonus.qualifies(weapon):
                    weapon_damage_list.append('{} [{}]'.format(bonus.attack_bonus, bonus.name))

            bonuses[weapon.name] = {
                'weapon': weapon,
                'attack_bonus': attack_bonus,
                'attack_type': attack_type,
                'damage': ' + '.join(weapon_damage_list),
            }
        return bonuses
