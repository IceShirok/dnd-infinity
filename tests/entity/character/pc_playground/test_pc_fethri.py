import unittest

from ddddd import pc_playground


class TestPlayerCharacterFethriLevel1(unittest.TestCase):
    """
    For the sake of sanity, I'll use pre-made characters
    to test out the rigor. It should cover most cases,
    if the other pieces (race, vocation, background, etc.)
    haven't caught these cases already.
    """
    def setUp(self):
        self.fethri = pc_playground.create_fethri(1)

    def test_name(self):
        self.assertEqual(self.fethri.name, 'Fethri Winterwhisper')

    def test_race_name(self):
        self.assertEqual(self.fethri.race_name, 'Tiefling')

    def test_base_race_name(self):
        self.assertEqual(self.fethri.base_race_name, 'Tiefling')

    def test_vocation_name(self):
        self.assertEqual(self.fethri.vocation_name, 'Rogue')

    def test_level(self):
        self.assertEqual(self.fethri.level, 1)

    def test_background(self):
        self.assertEqual(self.fethri.background_name, 'Noble')

    def test_proficiency_bonus(self):
        self.assertEqual(self.fethri.proficiency_bonus, 2)

    def test_speed(self):
        self.assertEqual(self.fethri.speed, 30)

    def test_size(self):
        self.assertEqual(self.fethri.size, 'medium')

    def test_ability_scores(self):
        ability_scores = self.fethri.ability_scores
        self.assertEqual(ability_scores['STR'].score, 10)
        self.assertEqual(ability_scores['DEX'].score, 14)
        self.assertEqual(ability_scores['CON'].score, 12)
        self.assertEqual(ability_scores['INT'].score, 16)
        self.assertEqual(ability_scores['WIS'].score, 11)
        self.assertEqual(ability_scores['CHA'].score, 14)

    def test_armor_class(self):
        self.assertEqual(self.fethri.armor_class, 13)

    def test_initiative(self):
        self.assertEqual(self.fethri.initiative, 2)

    #########################
    # HIT POINTS
    #########################

    def test_max_hit_points(self):
        self.assertEqual(self.fethri.max_hit_points, 9)

    def test_total_hit_die(self):
        self.assertEqual(self.fethri.total_hit_dice, {'d8': 1})

    def total_hit_dice_prettified(self):
        self.assertEqual(self.fethri.total_hit_dice_prettified, '1d8')

    #########################
    # PROFICIENCIES
    #########################

    def test_saving_throws(self):
        saves = self.fethri.saving_throws
        result = dict(map(lambda s: (s, {'modifier': saves[s].modifier, 'is_proficient': saves[s].is_proficient}), saves))
        expected = {
            'STR': {
                'modifier': 0,
                'is_proficient': False,
            },
            'DEX': {
                'modifier': 4,
                'is_proficient': True,
            },
            'CON': {
                'modifier': 1,
                'is_proficient': False,
            },
            'INT': {
                'modifier': 5,
                'is_proficient': True,
            },
            'WIS': {
                'modifier': 0,
                'is_proficient': False,
            },
            'CHA': {
                'modifier': 2,
                'is_proficient': False,
            },
        }
        self.assertEqual(expected, result)

    def test_skills_by_ability(self):
        skillz = self.fethri.skills_by_ability

        athletics = skillz['STR']['Athletics']
        self.assertEqual(athletics.ability, 'STR')
        self.assertEqual(athletics.is_proficient, False)
        self.assertEqual(athletics.expertise, False)
        self.assertEqual(athletics.modifier, 0)

        stealth = skillz['DEX']['Stealth']
        self.assertEqual(stealth.ability, 'DEX')
        self.assertEqual(stealth.is_proficient, True)
        self.assertEqual(stealth.expertise, False)
        self.assertEqual(stealth.modifier, 4)

        investigation = skillz['INT']['Investigation']
        self.assertEqual(investigation.ability, 'INT')
        self.assertEqual(investigation.is_proficient, True)
        self.assertEqual(investigation.expertise, True)
        self.assertEqual(investigation.modifier, 7)

    def test_proficiencies(self):
        prof = self.fethri.proficiencies
        self.assertEqual(set(prof['Weapon Proficiency']), {'rapier', 'longsword', 'hand crossbow', 'simple', 'shortsword'})
        self.assertEqual(len(prof['Armor Proficiency']), 1)
        self.assertEqual(len(prof['Tool Proficiency']), 2)

    def test_languages(self):
        lang = self.fethri.languages
        self.assertEqual(len(lang), 4)

    #########################
    # FEATURES & TRAITS
    #########################

    def test_feats(self):
        self.assertEqual(self.fethri.feats, [])

    def test_racial_traits(self):
        self.assertEqual(len(self.fethri.racial_traits), 3)

    def test_vocation_features(self):
        self.assertEqual(len(self.fethri.vocation_features), 3)

    def test_background_feature(self):
        self.assertEqual(len(self.fethri.background_feature), 1)

    def test_features(self):
        features = self.fethri.features
        self.assertEqual(features['Racial Traits'], self.fethri.racial_traits)
        self.assertEqual(features['Class Features'], self.fethri.vocation_features)
        self.assertEqual(features['Background Features'], list(self.fethri.background_feature))

    #########################
    # SPELLCASTING
    #########################

    def test_spellcasting(self):
        self.assertEqual(self.fethri.spellcasting, None)

    def test_cantrips(self):
        self.assertEqual(self.fethri.cantrips, None)

    def test_calculate_damage_cantrips(self):
        self.assertEqual(self.fethri.calculate_damage_cantrips(), {})

    def test_casting_spells(self):
        self.assertEqual(self.fethri.casting_spells, None)

    def test_spell_attack_bonus(self):
        self.assertEqual(self.fethri.spell_attack_bonus, None)

    def test_spell_save_dc(self):
        self.assertEqual(self.fethri.spell_save_dc, None)

    #########################
    # EQUIPMENT
    #########################

    def test_carrying_weight(self):
        self.assertEqual(self.fethri.carrying_weight, 67)

    def test_carrying_capacity(self):
        self.assertEqual(self.fethri.carrying_capacity, 150)

    def test_calculate_weapon_bonuses(self):
        weapon_bonuses = self.fethri.calculate_weapon_bonuses()

        weapon_bonus_list = set(weapon_bonuses.keys())
        weapons_list = set(map(lambda w: w.name, self.fethri.worn_items.weapons))
        self.assertEqual(weapon_bonus_list, weapons_list)

        rapier_bonus = weapon_bonuses['rapier']
        self.assertEqual(rapier_bonus['attack_bonus'], 4)
        self.assertEqual(rapier_bonus['attack_type'], 'DEX')
        self.assertEqual(rapier_bonus['damage'], '1d8 piercing + 2 + 1d6 [Sneak Attack]')


class TestPlayerCharacterFethriLevel4(unittest.TestCase):
    def setUp(self):
        self.fethri = pc_playground.create_fethri(4)

    def test_name(self):
        self.assertEqual(self.fethri.name, 'Fethri Winterwhisper')

    def test_race_name(self):
        self.assertEqual(self.fethri.race_name, 'Tiefling')

    def test_base_race_name(self):
        self.assertEqual(self.fethri.base_race_name, 'Tiefling')

    def test_vocation_name(self):
        self.assertEqual(self.fethri.vocation_name, 'Rogue')

    def test_level(self):
        self.assertEqual(self.fethri.level, 4)

    def test_background(self):
        self.assertEqual(self.fethri.background_name, 'Noble')

    def test_proficiency_bonus(self):
        self.assertEqual(self.fethri.proficiency_bonus, 2)

    def test_speed(self):
        self.assertEqual(self.fethri.speed, 30)

    def test_size(self):
        self.assertEqual(self.fethri.size, 'medium')

    def test_ability_scores(self):
        ability_scores = self.fethri.ability_scores
        self.assertEqual(ability_scores['STR'].score, 10)
        self.assertEqual(ability_scores['DEX'].score, 16)
        self.assertEqual(ability_scores['CON'].score, 12)
        self.assertEqual(ability_scores['INT'].score, 16)
        self.assertEqual(ability_scores['WIS'].score, 11)
        self.assertEqual(ability_scores['CHA'].score, 14)

    def test_armor_class(self):
        self.assertEqual(self.fethri.armor_class, 14)

    def test_initiative(self):
        self.assertEqual(self.fethri.initiative, 3)

    #########################
    # HIT POINTS
    #########################

    def test_max_hit_points(self):
        self.assertEqual(self.fethri.max_hit_points, 27)

    def test_total_hit_die(self):
        self.assertEqual(self.fethri.total_hit_dice, {'d8': 4})

    def total_hit_dice_prettified(self):
        self.assertEqual(self.fethri.total_hit_dice_prettified, '4d8')

    #########################
    # PROFICIENCIES
    #########################

    def test_saving_throws(self):
        saves = self.fethri.saving_throws
        result = dict(map(lambda s: (s, {'modifier': saves[s].modifier, 'is_proficient': saves[s].is_proficient}), saves))
        expected = {
            'STR': {
                'modifier': 0,
                'is_proficient': False,
            },
            'DEX': {
                'modifier': 5,
                'is_proficient': True,
            },
            'CON': {
                'modifier': 1,
                'is_proficient': False,
            },
            'INT': {
                'modifier': 5,
                'is_proficient': True,
            },
            'WIS': {
                'modifier': 0,
                'is_proficient': False,
            },
            'CHA': {
                'modifier': 2,
                'is_proficient': False,
            },
        }
        self.assertEqual(expected, result)

    def test_skills_by_ability(self):
        skillz = self.fethri.skills_by_ability

        athletics = skillz['STR']['Athletics']
        self.assertEqual(athletics.ability, 'STR')
        self.assertEqual(athletics.is_proficient, False)
        self.assertEqual(athletics.expertise, False)
        self.assertEqual(athletics.modifier, 0)

        stealth = skillz['DEX']['Stealth']
        self.assertEqual(stealth.ability, 'DEX')
        self.assertEqual(stealth.is_proficient, True)
        self.assertEqual(stealth.expertise, False)
        self.assertEqual(stealth.modifier, 5)

        investigation = skillz['INT']['Investigation']
        self.assertEqual(investigation.ability, 'INT')
        self.assertEqual(investigation.is_proficient, True)
        self.assertEqual(investigation.expertise, True)
        self.assertEqual(investigation.modifier, 7)

    def test_proficiencies(self):
        prof = self.fethri.proficiencies
        self.assertEqual(set(prof['Weapon Proficiency']), {'rapier', 'longsword', 'hand crossbow', 'simple', 'shortsword'})
        self.assertEqual(len(prof['Armor Proficiency']), 1)
        self.assertEqual(len(prof['Tool Proficiency']), 5)

    def test_languages(self):
        lang = self.fethri.languages
        self.assertEqual(len(lang), 6)

    #########################
    # FEATURES & TRAITS
    #########################

    def test_feats(self):
        self.assertEqual(self.fethri.feats, [])

    def test_racial_traits(self):
        self.assertEqual(len(self.fethri.racial_traits), 3)

    def test_vocation_features(self):
        self.assertEqual(len(self.fethri.vocation_features), 7)

    def test_background_feature(self):
        self.assertEqual(len(self.fethri.background_feature), 1)

    def test_features(self):
        features = self.fethri.features
        self.assertEqual(features['Racial Traits'], self.fethri.racial_traits)
        self.assertEqual(features['Class Features'], self.fethri.vocation_features)
        self.assertEqual(features['Background Features'], list(self.fethri.background_feature))

    #########################
    # SPELLCASTING
    #########################

    def test_spellcasting(self):
        self.assertEqual(self.fethri.spellcasting, None)

    def test_cantrips(self):
        self.assertEqual(self.fethri.cantrips, None)

    def test_calculate_damage_cantrips(self):
        self.assertEqual(self.fethri.calculate_damage_cantrips(), {})

    def test_casting_spells(self):
        self.assertEqual(self.fethri.casting_spells, None)

    def test_spell_attack_bonus(self):
        self.assertEqual(self.fethri.spell_attack_bonus, None)

    def test_spell_save_dc(self):
        self.assertEqual(self.fethri.spell_save_dc, None)

    #########################
    # EQUIPMENT
    #########################

    def test_carrying_weight(self):
        self.assertEqual(self.fethri.carrying_weight, 67)

    def test_carrying_capacity(self):
        self.assertEqual(self.fethri.carrying_capacity, 150)

    def test_calculate_weapon_bonuses(self):
        weapon_bonuses = self.fethri.calculate_weapon_bonuses()

        weapon_bonus_list = set(weapon_bonuses.keys())
        weapons_list = set(map(lambda w: w.name, self.fethri.worn_items.weapons))
        self.assertEqual(weapon_bonus_list, weapons_list)

        rapier_bonus = weapon_bonuses['rapier']
        self.assertEqual(rapier_bonus['attack_bonus'], 5)
        self.assertEqual(rapier_bonus['attack_type'], 'DEX')
        self.assertEqual(rapier_bonus['damage'], '1d8 piercing + 3 + 2d6 [Sneak Attack]')
