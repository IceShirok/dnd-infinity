import unittest

from ddddd.entity.character.base import AbilityScoreIncrease
from ddddd.entity.character import vocation, feature, base


class TestVocation(unittest.TestCase):
    def setUp(self):
        prof = {
            base.ARMOR_PROFICIENCY: feature.ArmorProficiency(name='Armor Proficiency',
                                                             proficiencies=['light',
                                                                          'medium',
                                                                          'shields']),
            base.WEAPON_PROFICIENCY: feature.WeaponProficiency(name='Weapon Proficiency',

                                                               proficiencies=['simple',
                                                                            'martial']),
        }
        saves = ['STR', 'DEX']
        skills = ['Athletics', 'Acrobatics', 'Animal Handling']
        features = {
            'favored_enemy': feature.Feature(name='Favored Enemy', description=''),
            'favored_terrain': feature.Feature(name='Favored Terrain', description=''),
        }
        self.vocation = vocation.Vocation(name='Vocation',
                                          level=1,
                                          hit_die=10,
                                          proficiencies=prof,
                                          saving_throws=saves,
                                          skill_proficiencies=skills,
                                          features=features)

    def test_features(self):
        result = self.vocation.features
        self.assertEqual(len(result), 2)
        self.assertTrue(isinstance(result, list))

    def test_append_feature_add(self):
        self.vocation._append_feature('favored_flavor', feature.Feature(name='Favored Flavor', description=''))
        result = self.vocation.features

        self.assertEqual(len(result), 3)

    def test_append_feature_replace(self):
        self.vocation._append_feature('favored_terrain', feature.Feature(name='Improved Favored Terrain', description=''))
        result = self.vocation.features

        self.assertEqual(len(result), 2)

        replaced = list(filter(lambda x: x.name == 'Improved Favored Terrain', result))
        self.assertEqual(len(replaced), 1)

    def test_languages(self):
        self.vocation._append_feature('language_1', feature.LanguagesKnown(languages=['elvish', 'dwarvish']))
        self.vocation._append_feature('language_2', feature.LanguagesKnown(languages=['draconic', 'undercommon']))
        result = self.vocation.languages

        self.assertEqual(len(result.languages), 4)

    def test_aggregate_asi(self):
        kwargs = {
            'ability_score_increase_1': {
                'STR': AbilityScoreIncrease('STR', 1),
                'CON': AbilityScoreIncrease('CON', 1),
            },
        }
        self.vocation._aggregate_asi_or_feat(kwargs, level=1)
        self.assertEqual(self.vocation.asi['STR'].score_increase, 1)
        self.assertEqual(self.vocation.asi['CON'].score_increase, 1)

        kwargs = {
            'ability_score_increase_2': {
                'STR': AbilityScoreIncrease('STR', 1),
                'WIS': AbilityScoreIncrease('WIS', 1),
            },
        }
        self.vocation._aggregate_asi_or_feat(kwargs, level=2)
        self.assertEqual(self.vocation.asi['STR'].score_increase, 2)
        self.assertEqual(self.vocation.asi['CON'].score_increase, 1)
        self.assertEqual(self.vocation.asi['WIS'].score_increase, 1)

    def test_aggregate_feat(self):
        kwargs = {
            'feat_1': feature.Feature(name='feat', description=''),
        }
        self.vocation._aggregate_asi_or_feat(kwargs, level=1)
        self.assertEqual(len(self.vocation.feats), 1)

        kwargs = {
            'feat_2': feature.Feature(name='feat', description=''),
        }
        self.vocation._aggregate_asi_or_feat(kwargs, level=2)
        self.assertEqual(len(self.vocation.feats), 2)

    def test_level_to_good_input(self):
        self.vocation.level_to(20)

    def test_level_to_bad_input(self):
        # Test upper bounds
        with self.assertRaises(ValueError):
            self.vocation.level_to(21)

        # Test to make sure you can't go backwards
        with self.assertRaises(ValueError):
            self.vocation.level_to(1)

        # Test to make sure you can't go backwards
        self.vocation.level_to(5)
        with self.assertRaises(ValueError):
            self.vocation.level_to(5)
