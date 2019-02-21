import unittest

from ddddd.entity import base
from ddddd.entity.base import Skills
from ddddd.entity.character import race, feature, pc, background
from ddddd.entity.character.vocations import ranger
from ddddd.items import items, armor, weapons


class TestPlayerBase(unittest.TestCase):
    def setUp(self):
        self.pc_base = pc.PlayerBase('Bob', 15, 14, 13, 12, 10, 8)

    def test_base_ability_scores(self):
        scores = self.pc_base.base_ability_scores
        result_count = list(filter(lambda a: isinstance(a, base.AbilityScore), scores.values()))
        self.assertEqual(len(result_count), 6)

    def test_proficiency_bonus(self):
        prof_list = [
            (1, 2), (2, 2), (3, 2), (4, 2),
            (5, 3), (6, 3), (7, 3), (8, 3),
            (9, 4), (10, 4), (11, 4), (12, 4),
            (13, 5), (14, 5), (15, 5), (16, 5),
            (17, 6), (18, 6), (19, 6), (20, 6)
        ]
        for i in range(0, 20):
            level = i+1
            self.pc_base.level = level
            result = self.pc_base.proficiency_bonus
            self.assertEqual((level, result), prof_list[i])


class TestPlayerCharacterDorian(unittest.TestCase):
    """
    For the sake of sanity, I'll use pre-made characters
    to test out the rigor. It should cover most cases,
    if the other pieces (race, vocation, background, etc.)
    haven't caught these cases already.
    """
    def setUp(self):
        base_ = pc.PlayerBase("Dorian Sapbleden", 16, 10, 14, 12, 14, 8, level=1)
        tool_prof = [
            feature.ToolProficiency(name='Tool Proficiency',
                                    proficiencies=['brewers_kit'])
        ]
        race_ = race.HillDwarf(traits=tool_prof)
        vocation = ranger.Ranger(skill_proficiencies=[Skills.ATHLETICS, Skills.ANIMAL_HANDLING, Skills.SURVIVAL],
                                 favored_enemy='plants',
                                 languages='elvish',
                                 favored_terrain='forest')
        bg = background.Criminal()

        worn_items = items.WornItems()
        worn_items.don_armor(armor.CHAIN_MAIL)
        worn_items.equip_weapon(weapons.HANDAXE)
        worn_items.equip_weapon(weapons.HANDAXE)
        worn_items.equip_weapon(weapons.LONGBOW)

        backpack = items.generate_burglars_pack()
        backpack.add_item(armor.CHAIN_SHIRT)
        backpack.add_item(armor.LEATHER_ARMOR)

        self.dorian = pc.PlayerCharacter(base_, race_, vocation, bg, worn_items, backpack)

    def test_name(self):
        self.assertEqual(self.dorian.name, 'Dorian Sapbleden')

    def test_race_name(self):
        self.assertEqual(self.dorian.race_name, 'Hill Dwarf')

    def test_base_race_name(self):
        self.assertEqual(self.dorian.base_race_name, 'Dwarf')

    def test_vocation_name(self):
        self.assertEqual(self.dorian.vocation_name, 'Ranger')

    def test_level(self):
        self.assertEqual(self.dorian.level, 1)

    def test_background(self):
        self.assertEqual(self.dorian.background_name, 'Criminal')

    def test_proficiency_bonus(self):
        self.assertEqual(self.dorian.proficiency_bonus, 2)

    def test_speed(self):
        self.assertEqual(self.dorian.speed, 25)

    def test_size(self):
        self.assertEqual(self.dorian.size, 'medium')

    def test_ability_scores(self):
        ability_scores = self.dorian.ability_scores
        self.assertEqual(ability_scores['STR'].score, 16)
        self.assertEqual(ability_scores['DEX'].score, 10)
        self.assertEqual(ability_scores['CON'].score, 16)
        self.assertEqual(ability_scores['INT'].score, 12)
        self.assertEqual(ability_scores['WIS'].score, 15)
        self.assertEqual(ability_scores['CHA'].score, 8)

    def test_armor_class(self):
        self.assertEqual(self.dorian.armor_class, 16)

    def test_initiative(self):
        self.assertEqual(self.dorian.initiative, 0)

    #########################
    # HIT POINTS
    #########################

    def test_max_hit_points(self):
        self.assertEqual(self.dorian.max_hit_points, 14)

    def test_total_hit_die(self):
        self.assertEqual(self.dorian.total_hit_dice, {'d10': 1})

    def total_hit_dice_prettified(self):
        self.assertEqual(self.dorian.total_hit_dice_prettified, '1d10')

    #########################
    # PROFICIENCIES
    #########################

    def test_saving_throws(self):
        saves = self.dorian.saving_throws
        expected = {
            'STR': {
                'modifier': 5,
                'is_proficient': True,
            },
            'DEX': {
                'modifier': 2,
                'is_proficient': True,
            },
            'CON': {
                'modifier': 3,
                'is_proficient': False,
            },
            'INT': {
                'modifier': 1,
                'is_proficient': False,
            },
            'WIS': {
                'modifier': 2,
                'is_proficient': False,
            },
            'CHA': {
                'modifier': -1,
                'is_proficient': False,
            },
        }
        self.assertEqual(saves, expected)

    def test_skills_by_ability(self):
        skillz = self.dorian.skills_by_ability

        athletics = skillz['STR']['Athletics']
        self.assertEqual(athletics['ability'], 'STR')
        self.assertEqual(athletics['is_proficient'], True)
        self.assertEqual(athletics['expertise'], False)

        athletics = skillz['DEX']['Acrobatics']
        self.assertEqual(athletics['ability'], 'DEX')
        self.assertEqual(athletics['is_proficient'], False)
        self.assertEqual(athletics['expertise'], False)

    def test_proficiencies(self):
        prof = self.dorian.proficiencies
        self.assertEqual(set(prof['Weapon Proficiency']), {'simple', 'martial'})
        self.assertEqual(len(prof['Armor Proficiency']), 3)
        self.assertEqual(len(prof['Tool Proficiency']), 3)

    def test_languages(self):
        lang = self.dorian.languages
        self.assertEqual(len(lang), 3)

    #########################
    # FEATURES & TRAITS
    #########################

    def test_feats(self):
        self.assertEqual(self.dorian.feats, [])

    def test_racial_traits(self):
        self.assertEqual(len(self.dorian.racial_traits), 6)

    def test_vocation_features(self):
        self.assertEqual(len(self.dorian.vocation_features), 3)

    def test_background_feature(self):
        self.assertEqual(len(self.dorian.background_feature), 1)

    def test_features(self):
        features = self.dorian.features
        self.assertEqual(features['Racial Traits'], self.dorian.racial_traits)
        self.assertEqual(features['Class Features'], self.dorian.vocation_features)
        self.assertEqual(features['Background Features'], list(self.dorian.background_feature))

    #########################
    # SPELLCASTING
    #########################

    def test_spellcasting(self):
        self.assertEqual(self.dorian.spellcasting, None)

    def test_cantrips(self):
        self.assertEqual(self.dorian.cantrips, None)

    def test_calculate_damage_cantrips(self):
        self.assertEqual(self.dorian.calculate_damage_cantrips(), {})

    def test_casting_spells(self):
        self.assertEqual(self.dorian.casting_spells, None)

    def test_spell_attack_bonus(self):
        self.assertEqual(self.dorian.spell_attack_bonus, None)

    def test_spell_save_dc(self):
        self.assertEqual(self.dorian.spell_save_dc, None)

    #########################
    # EQUIPMENT
    #########################

    def test_carrying_weight(self):
        self.assertEqual(self.dorian.carrying_weight, 146)

    def test_carrying_capacity(self):
        self.assertEqual(self.dorian.carrying_capacity, 240)

    def test_calculate_weapon_bonuses(self):
        weapon_bonuses = self.dorian.calculate_weapon_bonuses()

        weapon_bonus_list = set(weapon_bonuses.keys())
        weapons_list = set(map(lambda w: w.name, self.dorian.worn_items.weapons))
        self.assertEqual(weapon_bonus_list, weapons_list)

        handaxe_bonus = weapon_bonuses['handaxe']
        self.assertEqual(handaxe_bonus['attack_bonus'], 5)
        self.assertEqual(handaxe_bonus['attack_type'], 'STR')
        self.assertEqual(handaxe_bonus['damage'], '1d6 slashing + 3')

        handaxe_bonus = weapon_bonuses['longbow']
        self.assertEqual(handaxe_bonus['attack_bonus'], 2)
        self.assertEqual(handaxe_bonus['attack_type'], 'DEX')
        self.assertEqual(handaxe_bonus['damage'], '1d8 piercing')
