import unittest
from ddddd.items import armor


class TestArmorClass(unittest.TestCase):
    def test_light_armor_rating(self):
        self.assertEqual(14, armor.calc_light_armor_rating(3))

    def test_medium_armor_rating(self):
        self.assertEqual(14, armor.calc_medium_armor_rating(1))
        self.assertEqual(15, armor.calc_medium_armor_rating(3))

    def test_heavy_armor_rating(self):
        self.assertEqual(16, armor.calc_heavy_armor_rating())
