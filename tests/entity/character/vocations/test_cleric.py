import unittest

from ddddd.entity import base
from ddddd.entity.base import Skills
from ddddd.entity.character import feature, spells
from ddddd.entity.character.vocations import ranger, cleric


class TestClericLevel1(unittest.TestCase):
    def setUp(self):
        class_languages = feature.LanguagesKnown(languages=[base.Languages.DRACONIC, base.Languages.DWARVISH])
        class_cantrips = [spells.SACRED_FLAME, spells.GUIDANCE, spells.SPARE_THE_DYING]
        self.cleric = cleric.Cleric(skill_proficiencies=[Skills.INSIGHT, Skills.RELIGION, Skills.ARCANA, Skills.PERSUASION],
                                    languages=class_languages, cantrips=class_cantrips)

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
        # self.assertEqual(None, self.cleric.spellcasting)
        pass

    def test_asi(self):
        self.assertEqual({}, self.cleric.asi)


class TestClericLevel4(unittest.TestCase):
    def setUp(self):
        class_languages = feature.LanguagesKnown(languages=[base.Languages.DRACONIC, base.Languages.DWARVISH])
        class_cantrips = [spells.SACRED_FLAME, spells.GUIDANCE, spells.SPARE_THE_DYING]
        self.cleric = cleric.Cleric(skill_proficiencies=[Skills.INSIGHT, Skills.RELIGION, Skills.ARCANA, Skills.PERSUASION],
                                    languages=class_languages, cantrips=class_cantrips)

        self.cleric.level_to(level=4,
                             cantrip_4=spells.WORD_OF_RADIANCE,
                             ability_score_increase_4={
                                 base.AbilityScore.WIS: base.AbilityScoreIncrease(base.AbilityScore.WIS, 2),
                             })

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
        # self.assertTrue(self.cleric.spellcasting is None)
        pass

    def test_asi(self):
        self.assertEqual({'WIS'}, set(self.cleric.asi.keys()))
