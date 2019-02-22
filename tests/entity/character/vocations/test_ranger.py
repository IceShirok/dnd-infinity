import unittest

from ddddd.entity import base
from ddddd.entity.base import Skills
from ddddd.entity.character.vocations import ranger


class TestRangerLevel1(unittest.TestCase):
    def setUp(self):
        self.ranger = ranger.Ranger(skill_proficiencies=[Skills.ATHLETICS, Skills.ANIMAL_HANDLING, Skills.SURVIVAL],
                                    favored_enemy='plants',
                                    languages='elvish',
                                    favored_terrain='forest')

    def test_name(self):
        self.assertEqual('Ranger', self.ranger.name)

    def test_level(self):
        self.assertEqual(1, self.ranger.level)

    def test_hit_die(self):
        self.assertEqual(10, self.ranger.hit_die)

    def test_proficiencies(self):
        self.assertEqual(2, len(self.ranger.proficiencies))

    def test_saving_throws(self):
        self.assertEqual(['STR', 'DEX'], self.ranger.saving_throws)

    def test_features(self):
        self.assertEqual(3, len(self.ranger.features))

    def test_spellcasting(self):
        self.assertEqual(None, self.ranger.spellcasting)

    def test_asi(self):
        self.assertEqual({}, self.ranger.asi)


class TestRangerLevel4(unittest.TestCase):
    def setUp(self):
        self.ranger = ranger.Ranger(skill_proficiencies=[Skills.ATHLETICS, Skills.ANIMAL_HANDLING, Skills.SURVIVAL],
                                    favored_enemy='plants',
                                    languages='elvish',
                                    favored_terrain='forest')
        self.ranger.level_to(level=4,
                             fighting_style='two_weapon_fighting',
                             archetype_feature='colossus_slayer',
                             ability_score_increase_4={
                                 base.AbilityScore.STR: base.AbilityScoreIncrease(base.AbilityScore.STR, 2),
                             })

    def test_name(self):
        self.assertEqual('Ranger', self.ranger.name)

    def test_level(self):
        self.assertEqual(4, self.ranger.level)

    def test_hit_die(self):
        self.assertEqual(10, self.ranger.hit_die)

    def test_proficiencies(self):
        self.assertEqual(2, len(self.ranger.proficiencies))

    def test_saving_throws(self):
        self.assertEqual(['STR', 'DEX'], self.ranger.saving_throws)

    def test_features(self):
        self.assertEqual(6, len(self.ranger.features))

    def test_spellcasting(self):
        self.assertTrue(self.ranger.spellcasting is not None)

    def test_asi(self):
        self.assertEqual({'STR'}, set(self.ranger.asi.keys()))
