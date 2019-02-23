import unittest

from ddddd.entity.character import base


class TestPlayerBase(unittest.TestCase):
    def setUp(self):
        self.pc_base = base.EntityBase('Bob', 15, 14, 13, 12, 10, 8)

    def test_base_ability_scores(self):
        scores = self.pc_base.ability_scores
        result_count = list(filter(lambda a: isinstance(a, base.AbilityScore), scores.values()))
        self.assertEqual(len(result_count), 6)

    def test_proficiency_bonus(self):
        prof_list = [
            (1, 2), (2, 2), (3, 2), (4, 2),
            (5, 3), (6, 3), (7, 3), (8, 3),
            (9, 4), (10, 4), (11, 4), (12, 4),
            (13, 5), (14, 5), (15, 5), (16, 5),
            (17, 6), (18, 6), (19, 6), (20, 6)
        ]
        for i in range(0, 20):
            level = i+1
            self.pc_base.level = level
            result = self.pc_base.proficiency_bonus
            self.assertEqual((level, result), prof_list[i])
