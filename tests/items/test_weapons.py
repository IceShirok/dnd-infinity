import unittest

from ddddd.entity import base
from ddddd.items import weapons, currency


class TestWeaponFunctions(unittest.TestCase):
    def test_get_aggregated_weapon_proficiencies(self):
        proficiencies = ['mace', 'rapier']
        result = weapons.get_aggregated_weapon_proficiencies(proficiencies)
        expected = ['mace', 'rapier']
        self.assertEqual(expected, result)

    def test_get_aggregated_weapon_proficiencies_categories(self):
        proficiencies = ['simple', 'martial', 'mace', 'rapier']
        result = weapons.get_aggregated_weapon_proficiencies(proficiencies)
        expected = ['simple', 'martial']
        self.assertEqual(expected, result)

    def test_get_aggregated_weapon_proficiencies_simple(self):
        proficiencies = ['simple', 'mace', 'rapier']
        result = weapons.get_aggregated_weapon_proficiencies(proficiencies)
        expected = ['simple', 'rapier']
        self.assertEqual(expected, result)

    def test_get_aggregated_weapon_proficiencies_martial(self):
        proficiencies = ['martial', 'mace', 'rapier']
        result = weapons.get_aggregated_weapon_proficiencies(proficiencies)
        expected = ['martial', 'mace']
        self.assertEqual(expected, result)

    def test_determine_attack_bonus_type_melee(self):
        ability_scores = {
            'STR': base.AbilityScore('STR', 10),
            'DEX': base.AbilityScore('DEX', 14),
        }
        str_weapon = weapons.Weapon('Melee weapon', category=weapons.SIMPLE,
                                    damage='1d6 bludgeoning',
                                    price=currency.GoldPieces(5),
                                    weight=4,
                                    properties=[])
        result = weapons.determine_attack_bonus_type(str_weapon, ability_scores)
        self.assertEqual(('STR', 0), result)

    def test_determine_attack_bonus_type_ranged(self):
        ability_scores = {
            'STR': base.AbilityScore('STR', 10),
            'DEX': base.AbilityScore('DEX', 14),
        }
        str_weapon = weapons.Weapon('Ranged weapon', category=weapons.SIMPLE,
                                    damage='1d6 bludgeoning',
                                    price=currency.GoldPieces(5),
                                    weight=4,
                                    properties=['ammunition (range 150/600)'])
        result = weapons.determine_attack_bonus_type(str_weapon, ability_scores)
        self.assertEqual(('DEX', 2), result)

    def test_determine_attack_bonus_type_finesse(self):
        ability_scores = {
            'STR': base.AbilityScore('STR', 10),
            'DEX': base.AbilityScore('DEX', 14),
        }
        str_weapon = weapons.Weapon('Finesse weapon', category=weapons.SIMPLE,
                                    damage='1d6 bludgeoning',
                                    price=currency.GoldPieces(5),
                                    weight=4,
                                    properties=['finesse'])
        result = weapons.determine_attack_bonus_type(str_weapon, ability_scores)
        self.assertEqual(('DEX', 2), result)

    def test_is_proficient_weapon(self):
        proficiencies = ['mace', 'rapier']

        weapon = weapons.Weapon('Mace', category=weapons.SIMPLE,
                                damage='1d6 bludgeoning',
                                price=currency.GoldPieces(5),
                                weight=4,
                                properties=[])
        self.assertEqual(True, weapons.is_proficient(weapon, proficiencies))

        weapon = weapons.Weapon('Longsword', category=weapons.MARTIAL,
                                damage='1d6 bludgeoning',
                                price=currency.GoldPieces(5),
                                weight=4,
                                properties=[])
        self.assertEqual(False, weapons.is_proficient(weapon, proficiencies))

    def test_is_proficient_category(self):
        proficiencies = ['simple', 'rapier']

        weapon = weapons.Weapon('Mace', category=weapons.SIMPLE,
                                damage='1d6 bludgeoning',
                                price=currency.GoldPieces(5),
                                weight=4,
                                properties=[])
        self.assertEqual(True, weapons.is_proficient(weapon, proficiencies))

        weapon = weapons.Weapon('Longsword', category=weapons.MARTIAL,
                                damage='1d6 bludgeoning',
                                price=currency.GoldPieces(5),
                                weight=4,
                                properties=[])
        self.assertEqual(False, weapons.is_proficient(weapon, proficiencies))
