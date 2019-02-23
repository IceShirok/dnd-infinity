import unittest

from ddddd.entity.character.base import Skills
from ddddd.entity.character import spells, base
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


class RangerSpellcastingAbility(unittest.TestCase):
    def setUp(self):
        simple_spell_list = [
            ('Hunters Mark', base.SpellTypes.FIRST),
            ('Animal Friendship', base.SpellTypes.FIRST),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)
        self.spellcasting = ranger.RangerSpellcastingAbility(spell_slots={'1st': 2},
                                                             casting_spells=casting_spells,
                                                             num_spells_known=2)

    def test_init(self):
        self.assertEqual('WIS', self.spellcasting.spellcasting_ability)
        self.assertEqual({'1st': 2}, self.spellcasting.spell_slots)
        self.assertEqual(2, len(self.spellcasting.casting_spells))
        self.assertEqual(0, self.spellcasting.num_cantrips_known)
        self.assertEqual(0, len(self.spellcasting.cantrips))
        self.assertEqual(2, self.spellcasting.num_spells_known)

    def test_spell_save_dc(self):
        ability_scores = {'WIS': base.AbilityScore('WIS', 16)}
        proficiency_bonus = 2
        self.assertEqual(13, self.spellcasting.spell_save_dc(ability_scores, proficiency_bonus))

    def test_spell_attack_bonus(self):
        ability_scores = {'WIS': base.AbilityScore('WIS', 16)}
        proficiency_bonus = 2
        self.assertEqual(5, self.spellcasting.spell_attack_bonus(ability_scores, proficiency_bonus))


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

        spellcasting = self.ranger.spellcasting
        self.assertEqual('WIS', spellcasting.spellcasting_ability)
        self.assertEqual({'1st': 3}, spellcasting.spell_slots)
        self.assertEqual(3, len(spellcasting.casting_spells))
        self.assertEqual(0, spellcasting.num_cantrips_known)
        self.assertEqual(0, len(spellcasting.cantrips))
        self.assertEqual(3, spellcasting.num_spells_known)

    def test_asi(self):
        self.assertEqual({'STR'}, set(self.ranger.asi.keys()))
