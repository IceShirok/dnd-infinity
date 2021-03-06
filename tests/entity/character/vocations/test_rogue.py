import unittest

from ddddd.entity.character.base import Skills
from ddddd.entity.character import feature, base
from ddddd.entity.character.vocations import rogue


class TestRogueLevel1(unittest.TestCase):
    def setUp(self):
        self.rogue = rogue.Rogue(skill_proficiencies=[Skills.INVESTIGATION,
                                                      Skills.DECEPTION,
                                                      Skills.STEALTH],
                                 expertise=feature.Expertise(skills=[Skills.INVESTIGATION,
                                                                     Skills.DECEPTION],
                                                             proficiencies=None)
                                 )

    def test_name(self):
        self.assertEqual('Rogue', self.rogue.name)

    def test_level(self):
        self.assertEqual(1, self.rogue.level)

    def test_hit_die(self):
        self.assertEqual(8, self.rogue.hit_die)

    def test_proficiencies(self):
        self.assertEqual(3, len(self.rogue.proficiencies))

    def test_saving_throws(self):
        self.assertEqual(['DEX', 'INT'], self.rogue.saving_throws)

    def test_features(self):
        self.assertEqual(3, len(self.rogue.features))

    def test_spellcasting(self):
        self.assertEqual(None, self.rogue.spellcasting)

    def test_asi(self):
        self.assertEqual({}, self.rogue.asi)


class TestRogueLevel4(unittest.TestCase):
    def setUp(self):
        self.rogue = rogue.Rogue(skill_proficiencies=[Skills.INVESTIGATION,
                                                      Skills.DECEPTION,
                                                      Skills.STEALTH],
                                 expertise=feature.Expertise(skills=[Skills.INVESTIGATION,
                                                                     Skills.DECEPTION],
                                                             proficiencies=None)
                                 )
        self.rogue.level_to(level=4,
                            roguish_archetype='mastermind',
                            gaming_set='bone_dice',
                            languages=feature.LanguagesKnown(languages=[base.Languages.UNDERCOMMON,
                                                                        base.Languages.ELVISH]),
                            ability_score_increase_4={
                                base.AbilityScore.DEX: base.AbilityScoreIncrease(base.AbilityScore.DEX, 2),
                            })

    def test_name(self):
        self.assertEqual('Rogue', self.rogue.name)

    def test_level(self):
        self.assertEqual(4, self.rogue.level)

    def test_hit_die(self):
        self.assertEqual(8, self.rogue.hit_die)

    def test_proficiencies(self):
        self.assertEqual(3, len(self.rogue.proficiencies))

    def test_saving_throws(self):
        self.assertEqual(['DEX', 'INT'], self.rogue.saving_throws)

    def test_features(self):
        self.assertEqual(7, len(self.rogue.features))

    def test_spellcasting(self):
        self.assertEqual(None, self.rogue.spellcasting)

    def test_asi(self):
        self.assertEqual({'DEX'}, set(self.rogue.asi.keys()))


class TestRogueLevel4Thief(unittest.TestCase):
    def setUp(self):
        self.rogue = rogue.Rogue(skill_proficiencies=[Skills.INVESTIGATION,
                                                      Skills.DECEPTION,
                                                      Skills.STEALTH],
                                 expertise=feature.Expertise(skills=[Skills.INVESTIGATION,
                                                                     Skills.DECEPTION],
                                                             proficiencies=None)
                                 )
        self.rogue.level_to(level=4,
                            roguish_archetype='thief',
                            ability_score_increase_4={
                                base.AbilityScore.DEX: base.AbilityScoreIncrease(base.AbilityScore.DEX, 2),
                            })

    def test_name(self):
        self.assertEqual('Rogue', self.rogue.name)

    def test_level(self):
        self.assertEqual(4, self.rogue.level)

    def test_hit_die(self):
        self.assertEqual(8, self.rogue.hit_die)

    def test_proficiencies(self):
        self.assertEqual(3, len(self.rogue.proficiencies))

    def test_saving_throws(self):
        self.assertEqual(['DEX', 'INT'], self.rogue.saving_throws)

    def test_features(self):
        self.assertEqual(6, len(self.rogue.features))

    def test_spellcasting(self):
        self.assertEqual(None, self.rogue.spellcasting)

    def test_asi(self):
        self.assertEqual({'DEX'}, set(self.rogue.asi.keys()))


class TestRogueLevel20(unittest.TestCase):
    def setUp(self):
        self.rogue = rogue.Rogue(skill_proficiencies=[Skills.INVESTIGATION,
                                                      Skills.DECEPTION,
                                                      Skills.STEALTH],
                                 expertise=feature.Expertise(skills=[Skills.INVESTIGATION,
                                                                     Skills.DECEPTION],
                                                             proficiencies=None)
                                 )
        self.rogue.level_to(level=20,
                            roguish_archetype='mastermind',
                            gaming_set='bone_dice',
                            languages=feature.LanguagesKnown(languages=[base.Languages.UNDERCOMMON,
                                                                        base.Languages.ELVISH]),
                            ability_score_increase_4={
                                base.AbilityScore.DEX: base.AbilityScoreIncrease(base.AbilityScore.DEX, 2),
                            },
                            expertise_6=feature.Expertise(skills=[Skills.STEALTH],
                                                          proficiencies=['thieves_tools']),
                            ability_score_increase_8={
                                base.AbilityScore.DEX: base.AbilityScoreIncrease(base.AbilityScore.DEX, 2),
                            },
                            ability_score_increase_10={
                                base.AbilityScore.INT: base.AbilityScoreIncrease(base.AbilityScore.INT, 2),
                            },
                            ability_score_increase_12={
                                base.AbilityScore.DEX: base.AbilityScoreIncrease(base.AbilityScore.DEX, 2),
                            },
                            ability_score_increase_16={
                                base.AbilityScore.CHA: base.AbilityScoreIncrease(base.AbilityScore.CHA, 2),
                            },
                            ability_score_increase_19={
                                base.AbilityScore.INT: base.AbilityScoreIncrease(base.AbilityScore.INT, 2),
                            })

    def test_name(self):
        self.assertEqual('Rogue', self.rogue.name)

    def test_level(self):
        self.assertEqual(20, self.rogue.level)

    def test_hit_die(self):
        self.assertEqual(8, self.rogue.hit_die)

    def test_proficiencies(self):
        self.assertEqual(3, len(self.rogue.proficiencies))

    def test_saving_throws(self):
        self.assertEqual(['DEX', 'INT'], self.rogue.saving_throws)

    def test_features(self):
        self.assertEqual(17, len(self.rogue.features))

    def test_spellcasting(self):
        self.assertEqual(None, self.rogue.spellcasting)

    def test_asi(self):
        self.assertEqual({'DEX', 'INT', 'CHA'}, set(self.rogue.asi.keys()))
