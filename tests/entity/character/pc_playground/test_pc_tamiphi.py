import unittest

from ddddd import pc_playground


class TestPlayerCharacterTamiphiLevel1(unittest.TestCase):
    """
    For the sake of sanity, I'll use pre-made characters
    to test out the rigor. It should cover most cases,
    if the other pieces (race, vocation, background, etc.)
    haven't caught these cases already.
    """
    def setUp(self):
        self.tamiphi = pc_playground.create_tamiphi(1)

    def test_name(self):
        self.assertEqual(self.tamiphi.name, 'Tamiphi Tockentell')

    def test_race_name(self):
        self.assertEqual(self.tamiphi.race_name, 'Rock Gnome')

    def test_base_race_name(self):
        self.assertEqual(self.tamiphi.base_race_name, 'Gnome')

    def test_vocation_name(self):
        self.assertEqual(self.tamiphi.vocation_name, 'Cleric')

    def test_level(self):
        self.assertEqual(self.tamiphi.level, 1)

    def test_background(self):
        self.assertEqual(self.tamiphi.background_name, 'Sage')

    def test_proficiency_bonus(self):
        self.assertEqual(self.tamiphi.proficiency_bonus, 2)

    def test_speed(self):
        self.assertEqual(self.tamiphi.speed, 25)

    def test_size(self):
        self.assertEqual(self.tamiphi.size, 'small')

    def test_ability_scores(self):
        ability_scores = self.tamiphi.ability_scores
        self.assertEqual(ability_scores['STR'].score, 10)
        self.assertEqual(ability_scores['DEX'].score, 12)
        self.assertEqual(ability_scores['CON'].score, 16)
        self.assertEqual(ability_scores['INT'].score, 16)
        self.assertEqual(ability_scores['WIS'].score, 18)
        self.assertEqual(ability_scores['CHA'].score, 7)

    def test_armor_class(self):
        self.assertEqual(self.tamiphi.armor_class, 14)

    def test_initiative(self):
        self.assertEqual(self.tamiphi.initiative, 1)

    #########################
    # HIT POINTS
    #########################

    def test_max_hit_points(self):
        self.assertEqual(self.tamiphi.max_hit_points, 11)

    def test_total_hit_die(self):
        self.assertEqual(self.tamiphi.total_hit_dice, {'d8': 1})

    def total_hit_dice_prettified(self):
        self.assertEqual(self.tamiphi.total_hit_dice_prettified, '1d8s')

    #########################
    # PROFICIENCIES
    #########################

    def test_saving_throws(self):
        saves = self.tamiphi.saving_throws
        expected = {
            'STR': {
                'modifier': 0,
                'is_proficient': False,
            },
            'DEX': {
                'modifier': 1,
                'is_proficient': False,
            },
            'CON': {
                'modifier': 3,
                'is_proficient': False,
            },
            'INT': {
                'modifier': 3,
                'is_proficient': False,
            },
            'WIS': {
                'modifier': 6,
                'is_proficient': True,
            },
            'CHA': {
                'modifier': 0,
                'is_proficient': True,
            },
        }
        self.assertEqual(saves, expected)

    def test_skills_by_ability(self):
        skillz = self.tamiphi.skills_by_ability

        athletics = skillz['STR']['Athletics']
        self.assertEqual(athletics.ability, 'STR')
        self.assertEqual(athletics.is_proficient, False)
        self.assertEqual(athletics.expertise, False)
        self.assertEqual(athletics.modifier, 0)

        arcana = skillz['INT']['Arcana']
        self.assertEqual(arcana.ability, 'INT')
        self.assertEqual(arcana.is_proficient, True)
        self.assertEqual(arcana.expertise, True)
        self.assertEqual(arcana.modifier, 7)

        persuasion = skillz['CHA']['Persuasion']
        self.assertEqual(persuasion.ability, 'CHA')
        self.assertEqual(persuasion.is_proficient, True)
        self.assertEqual(persuasion.expertise, False)
        self.assertEqual(persuasion.modifier, 0)

    def test_proficiencies(self):
        prof = self.tamiphi.proficiencies
        self.assertEqual(set(prof['Weapon Proficiency']), {'simple'})
        self.assertEqual(len(prof['Armor Proficiency']), 3)
        self.assertEqual(len(prof['Tool Proficiency']), 1)

    def test_languages(self):
        lang = self.tamiphi.languages
        self.assertEqual(len(lang), 6)

    #########################
    # FEATURES & TRAITS
    #########################

    def test_feats(self):
        self.assertEqual(self.tamiphi.feats, [])

    def test_racial_traits(self):
        self.assertEqual(len(self.tamiphi.racial_traits), 4)

    def test_vocation_features(self):
        self.assertEqual(len(self.tamiphi.vocation_features), 3)

    def test_background_feature(self):
        self.assertEqual(len(self.tamiphi.background_feature), 1)

    def test_features(self):
        features = self.tamiphi.features
        self.assertEqual(features['Racial Traits'], self.tamiphi.racial_traits)
        self.assertEqual(features['Class Features'], self.tamiphi.vocation_features)
        self.assertEqual(features['Background Features'], list(self.tamiphi.background_feature))

    #########################
    # SPELLCASTING
    #########################

    def test_spellcasting(self):
        self.assertTrue(self.tamiphi.spellcasting is not None)

    def test_cantrips(self):
        self.assertEqual(len(self.tamiphi.cantrips), 3)

    def test_calculate_damage_cantrips(self):
        damage_cantrips = self.tamiphi.calculate_damage_cantrips()
        self.assertTrue('Sacred Flame' in damage_cantrips)

        sacred_flame = damage_cantrips['Sacred Flame']
        self.assertEqual('DEX DC 14', sacred_flame['attack_bonus'])
        self.assertEqual('1d8 fire', sacred_flame['damage'])

    def test_casting_spells(self):
        self.assertTrue('1st' in self.tamiphi.casting_spells)
        first_level_spells = self.tamiphi.casting_spells['1st']
        self.assertEqual(len(first_level_spells), 6)

    def test_spell_attack_bonus(self):
        self.assertEqual(self.tamiphi.spell_attack_bonus, 6)

    def test_spell_save_dc(self):
        self.assertEqual(self.tamiphi.spell_save_dc, 14)

    #########################
    # EQUIPMENT
    #########################

    def test_carrying_weight(self):
        self.assertEqual(self.tamiphi.carrying_weight, 68)

    def test_carrying_capacity(self):
        self.assertEqual(self.tamiphi.carrying_capacity, 150)

    def test_calculate_weapon_bonuses(self):
        weapon_bonuses = self.tamiphi.calculate_weapon_bonuses()

        weapon_bonus_list = set(weapon_bonuses.keys())
        weapons_list = set(map(lambda w: w.name, self.tamiphi.worn_items.weapons))
        self.assertEqual(weapon_bonus_list, weapons_list)

        handaxe_bonus = weapon_bonuses['mace']
        self.assertEqual(handaxe_bonus['attack_bonus'], 2)
        self.assertEqual(handaxe_bonus['attack_type'], 'STR')
        self.assertEqual(handaxe_bonus['damage'], '1d6 bludgeoning')
