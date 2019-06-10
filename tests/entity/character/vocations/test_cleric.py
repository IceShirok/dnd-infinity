import unittest

import ddddd.entity.character.spells
from ddddd.entity.character.base import Skills
from ddddd.entity.character import feature, spells, base
from ddddd.entity.character.vocations import cleric


class TestClericSpellcastingAbility(unittest.TestCase):
    def setUp(self):
        cantrips = [spells.SACRED_FLAME, spells.GUIDANCE, spells.SPARE_THE_DYING]
        self.spellcasting = cleric.ClericSpellcastingAbility(level=1,
                                                             cantrips=cantrips)
        self.ability_scores = {'WIS': base.AbilityScore(name='WIS', score=16)}

    def test_init(self):
        self.assertEqual('WIS', self.spellcasting.spellcasting_ability)
        self.assertEqual({'1st': 2}, self.spellcasting.spell_slots)
        self.assertEqual(1, self.spellcasting.level)
        self.assertEqual(0, len(self.spellcasting.casting_spells))
        self.assertEqual(3, self.spellcasting.num_cantrips_known)
        self.assertEqual(3, len(self.spellcasting.cantrips))
        self.assertEqual(4, self.spellcasting.num_spells_known(self.ability_scores))

    def test_spell_save_dc(self):
        ability_scores = {'WIS': base.AbilityScore('WIS', 16)}
        proficiency_bonus = 2
        self.assertEqual(13, self.spellcasting.spell_save_dc(ability_scores, proficiency_bonus))

    def test_spell_attack_bonus(self):
        ability_scores = {'WIS': base.AbilityScore('WIS', 16)}
        proficiency_bonus = 2
        self.assertEqual(5, self.spellcasting.spell_attack_bonus(ability_scores, proficiency_bonus))


class TestClericLevel1(unittest.TestCase):
    def setUp(self):
        class_languages = feature.LanguagesKnown(languages=[base.Languages.DRACONIC, base.Languages.DWARVISH])
        class_skills = [Skills.ARCANA, Skills.HISTORY]
        class_cantrips = [spells.SACRED_FLAME, spells.GUIDANCE, spells.SPARE_THE_DYING]
        self.cleric = cleric.Cleric(skill_proficiencies=[Skills.INSIGHT, Skills.RELIGION, Skills.ARCANA, Skills.PERSUASION],
                                    cleric_domain='knowledge', cantrips=class_cantrips,
                                    languages=class_languages, skills=class_skills)
        self.ability_scores = {'WIS': base.AbilityScore(name='WIS', score=16)}

    def test_name(self):
        self.assertEqual('Cleric', self.cleric.name)

    def test_level(self):
        self.assertEqual(1, self.cleric.level)

    def test_hit_die(self):
        self.assertEqual(8, self.cleric.hit_die)

    def test_proficiencies(self):
        self.assertEqual(2, len(self.cleric.proficiencies))

    def test_saving_throws(self):
        self.assertEqual(['WIS', 'CHA'], self.cleric.saving_throws)

    def test_features(self):
        self.assertEqual(3, len(self.cleric.features))

    def test_spellcasting(self):
        self.assertTrue(self.cleric.spellcasting is not None)

        spellcasting = self.cleric.spellcasting
        self.assertEqual('WIS', spellcasting.spellcasting_ability)
        self.assertEqual({'1st': 2}, spellcasting.spell_slots)
        self.assertEqual(2, len(spellcasting.casting_spells))
        self.assertEqual(3, spellcasting.num_cantrips_known)
        self.assertEqual(3, len(spellcasting.cantrips))
        self.assertEqual(4, spellcasting.num_spells_known(self.ability_scores))

    def test_spell_dc_with_ability(self):
        spell_dc = spells.spell_dc_with_ability('DEX')
        self.assertEqual('DEX DC 14', spell_dc(None, 14))

    def test_spell_attack(self):
        self.assertEqual('+5', spells.spell_attack('+5', None))

    def test_asi(self):
        self.assertEqual({}, self.cleric.asi)


class TestClericLevel4(unittest.TestCase):
    def setUp(self):
        class_languages = feature.LanguagesKnown(languages=[base.Languages.DRACONIC, base.Languages.DWARVISH])
        class_skills = [Skills.ARCANA, Skills.HISTORY]
        class_cantrips = [spells.SACRED_FLAME, spells.GUIDANCE, spells.SPARE_THE_DYING]
        self.cleric = cleric.Cleric(skill_proficiencies=[Skills.INSIGHT, Skills.RELIGION, Skills.ARCANA, Skills.PERSUASION],
                                    cleric_domain='knowledge', cantrips=class_cantrips,
                                    languages=class_languages, skills=class_skills)

        self.cleric.level_to(level=4,
                             cantrip_4=spells.WORD_OF_RADIANCE,
                             ability_score_increase_4={
                                 base.AbilityScore.WIS: base.AbilityScoreIncrease(base.AbilityScore.WIS, 2),
                             })
        self.ability_scores = {'WIS': base.AbilityScore(name='WIS', score=16)}

    def test_name(self):
        self.assertEqual('Cleric', self.cleric.name)

    def test_level(self):
        self.assertEqual(4, self.cleric.level)

    def test_hit_die(self):
        self.assertEqual(8, self.cleric.hit_die)

    def test_proficiencies(self):
        self.assertEqual(2, len(self.cleric.proficiencies))

    def test_saving_throws(self):
        self.assertEqual(['WIS', 'CHA'], self.cleric.saving_throws)

    def test_features(self):
        self.assertEqual(6, len(self.cleric.features))

    def test_spellcasting(self):
        self.assertTrue(self.cleric.spellcasting is not None)

        spellcasting = self.cleric.spellcasting
        self.assertEqual('WIS', spellcasting.spellcasting_ability)
        self.assertEqual({'1st': 4, '2nd': 3}, spellcasting.spell_slots)
        self.assertEqual(4, len(spellcasting.casting_spells))
        self.assertEqual(4, spellcasting.num_cantrips_known)
        self.assertEqual(4, len(spellcasting.cantrips))
        self.assertEqual(7, spellcasting.num_spells_known(self.ability_scores))

    def test_asi(self):
        self.assertEqual({'WIS'}, set(self.cleric.asi.keys()))
