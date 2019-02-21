import unittest

from ddddd.entity import base
from ddddd.entity.character import spells


class TestSpellFunctions(unittest.TestCase):
    def test_cantrips_by_level(self):
        self.assertEqual(3, spells.cantrips_by_level(1))
        self.assertEqual(3, spells.cantrips_by_level(4))
        self.assertEqual(4, spells.cantrips_by_level(5))
        self.assertEqual(4, spells.cantrips_by_level(10))
        self.assertEqual(5, spells.cantrips_by_level(11))
        self.assertEqual(5, spells.cantrips_by_level(20))


class TestDamageCantrip(unittest.TestCase):
    def setUp(self):
        pass


class TestSpellSlots(unittest.TestCase):
    def test_get_spell_slot_by_level(self):
        expected = {
            1: {'1st': 2},
            2: {'1st': 3},
            3: {'1st': 4, '2nd': 2},
            4: {'1st': 4, '2nd': 3},
            5: {'1st': 4, '2nd': 4, '3rd': 2},
            6: {'1st': 4, '2nd': 4, '3rd': 3},
            7: {'1st': 4, '2nd': 4, '3rd': 3, '4th': 1},
            8: {'1st': 4, '2nd': 4, '3rd': 3, '4th': 2},
            9: {'1st': 4, '2nd': 4, '3rd': 3, '4th': 3, '5th': 1},
            10: {'1st': 4, '2nd': 4, '3rd': 3, '4th': 3, '5th': 1},
            11: {'1st': 4, '2nd': 4, '3rd': 3, '4th': 3, '5th': 1, '6th': 1},
            12: {'1st': 4, '2nd': 4, '3rd': 3, '4th': 3, '5th': 1, '6th': 1},
            13: {'1st': 4, '2nd': 4, '3rd': 3, '4th': 3, '5th': 1, '6th': 1, '7th': 1},
            14: {'1st': 4, '2nd': 4, '3rd': 3, '4th': 3, '5th': 1, '6th': 1, '7th': 1},
            15: {'1st': 4, '2nd': 4, '3rd': 3, '4th': 3, '5th': 1, '6th': 1, '7th': 1, '8th': 1},
            16: {'1st': 4, '2nd': 4, '3rd': 3, '4th': 3, '5th': 1, '6th': 1, '7th': 1, '8th': 1},
            17: {'1st': 4, '2nd': 4, '3rd': 3, '4th': 3, '5th': 1, '6th': 1, '7th': 1, '8th': 1, '9th': 1},
            18: {'1st': 4, '2nd': 4, '3rd': 3, '4th': 3, '5th': 2, '6th': 1, '7th': 1, '8th': 1, '9th': 1},
            19: {'1st': 4, '2nd': 4, '3rd': 3, '4th': 3, '5th': 2, '6th': 2, '7th': 1, '8th': 1, '9th': 1},
            20: {'1st': 4, '2nd': 4, '3rd': 3, '4th': 3, '5th': 2, '6th': 2, '7th': 2, '8th': 1, '9th': 1},
        }
        for level in expected.keys():
            self.assertEqual(expected[level], spells.get_spell_slot_by_level(level))


class TestSpellcastingAbility(unittest.TestCase):
    def setUp(self):
        pass
