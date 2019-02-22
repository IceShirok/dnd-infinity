import unittest

from ddddd.entity import base
from ddddd.entity.character import spells


class TestSpellFunctions(unittest.TestCase):
    def test_cantrips_by_level(self):
        self.assertEqual(3, spells.cantrips_by_level(1))
        self.assertEqual(3, spells.cantrips_by_level(3))
        self.assertEqual(4, spells.cantrips_by_level(4))
        self.assertEqual(4, spells.cantrips_by_level(9))
        self.assertEqual(5, spells.cantrips_by_level(10))
        self.assertEqual(5, spells.cantrips_by_level(20))

    def test_spell_dc_with_ability(self):
        spell_dc = spells.spell_dc_with_ability('DEX')
        self.assertEqual('DEX DC 14', spell_dc(None, 14))

    def test_spell_attack(self):
        self.assertEqual('+5', spells.spell_attack('+5', None))

    def test_damage_by_level_with_dice(self):
        damage_by_level = spells.damage_by_level_with_dice('{}d100')
        self.assertEqual('1d100', damage_by_level(1))
        self.assertEqual('1d100', damage_by_level(4))
        self.assertEqual('2d100', damage_by_level(5))
        self.assertEqual('2d100', damage_by_level(10))
        self.assertEqual('3d100', damage_by_level(11))
        self.assertEqual('3d100', damage_by_level(16))
        self.assertEqual('4d100', damage_by_level(17))
        self.assertEqual('4d100', damage_by_level(20))


class TestDamageCantrip(unittest.TestCase):
    def setUp(self):
        self.damage_cantrip = spells.SACRED_FLAME

    def test_spell_level(self):
        self.assertEqual('cantrip', self.damage_cantrip.level)

    def test_calculate_attack_bonus(self):
        self.assertEqual('DEX DC 13', self.damage_cantrip.calculate_attack_bonus(5, 13))

    def test_calculate_damage_calc(self):
        self.assertEqual('1d8 fire', self.damage_cantrip.calculate_damage_calc(1))


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
        simple_spell_list = [
            ('Command', base.SpellTypes.FIRST),
            ('Identify', base.SpellTypes.FIRST),
            ('Cure Wounds', base.SpellTypes.FIRST),
            ('Bless', base.SpellTypes.FIRST),
            ('Healing Word', base.SpellTypes.FIRST),
            ('Sanctuary', base.SpellTypes.FIRST),
        ]
        cantrips = [spells.SACRED_FLAME, spells.GUIDANCE, spells.SPARE_THE_DYING]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)
        self.spellcasting = spells.SpellcastingAbility(spellcasting_ability='WIS',
                                                       spell_slots=spells.get_spell_slot_by_level(1),
                                                       casting_spells=casting_spells,
                                                       num_cantrips_known=spells.cantrips_by_level(3),
                                                       cantrips=cantrips)

    def test_spell_save_dc(self):
        ability_scores = {'WIS': base.AbilityScore('WIS', 16)}
        proficiency_bonus = 2
        self.assertEqual(13, self.spellcasting.spell_save_dc(ability_scores, proficiency_bonus))

    def test_spell_attack_bonus(self):
        ability_scores = {'WIS': base.AbilityScore('WIS', 16)}
        proficiency_bonus = 2
        self.assertEqual(5, self.spellcasting.spell_attack_bonus(ability_scores, proficiency_bonus))
