import unittest
from ddddd.entity import base


class TestFunctions(unittest.TestCase):
    def test_modifier(self):
        # test most extreme modifiers
        self.assertEqual(base.modifier(1), -5)
        self.assertEqual(base.modifier(20), 5)

        # test that the modifier changes correctly
        self.assertEqual(base.modifier(7), -2)
        self.assertEqual(base.modifier(8), -1)
        self.assertEqual(base.modifier(9), -1)
        self.assertEqual(base.modifier(10), 0)
        self.assertEqual(base.modifier(11), 0)
        self.assertEqual(base.modifier(12), 1)
        self.assertEqual(base.modifier(13), 1)

    def test_prettify_modifier(self):
        self.assertEqual(base.prettify_modifier(-1), '-1')
        self.assertEqual(base.prettify_modifier(0), '0')
        self.assertEqual(base.prettify_modifier(1), '+1')


class TestAbilityScoreIncrease(unittest.TestCase):
    def test_combine_good(self):
        asi1 = base.AbilityScoreIncrease('STR', 1)
        asi2 = base.AbilityScoreIncrease('STR', 2)
        result = asi1.combine(asi2)
        self.assertEqual(result.ability, 'STR')
        self.assertEqual(result.score_increase, 3)

    def test_combine_wrong_ability(self):
        asi1 = base.AbilityScoreIncrease('STR', 1)
        bad = base.AbilityScoreIncrease('WIS', 2)

        with self.assertRaises(ValueError):
            asi1.combine(bad)

    def test_combine_with_not_asi(self):
        asi1 = base.AbilityScoreIncrease('STR', 1)
        bad = base.AbilityScore('STR', 1)

        with self.assertRaises(ValueError):
            asi1.combine(bad)


class TestAbilityScore(unittest.TestCase):
    def test_modifier(self):
        ability = base.AbilityScore('STR', 15)
        self.assertEqual(ability.modifier, 2)

        ability = base.AbilityScore('STR', 7)
        self.assertEqual(ability.modifier, -2)

    def test_with_asi_good(self):
        ability = base.AbilityScore('STR', 15)
        asi = base.AbilityScoreIncrease('STR', 1)
        result = ability.with_ability_score_increase(asi)
        self.assertEqual(result.name, 'STR')
        self.assertEqual(result.score, 16)

    def test_with_asi_wrong_ability(self):
        ability = base.AbilityScore('STR', 15)
        bad = base.AbilityScoreIncrease('WIS', 1)

        with self.assertRaises(ValueError):
            ability.with_ability_score_increase(bad)

    def test_with_asi_with_not_asi(self):
        ability = base.AbilityScore('STR', 15)
        bad = base.AbilityScore('WIS', 1)

        with self.assertRaises(ValueError):
            ability.with_ability_score_increase(bad)
