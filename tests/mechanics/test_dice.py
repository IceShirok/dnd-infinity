import unittest
import random
from ddddd.mechanics import dice


class TestDiceFunctions(unittest.TestCase):
    def setUp(self):
        random.seed(13374343)

    def test_roll_die(self):
        die_type = 10
        expected = [4, 3, 1, 9, 9, 7, 10, 5, 6, 4]
        result = []
        for i in range(0, 10):
            roll = dice.roll_die(die_type)
            result.append(roll)
        self.assertEqual(result, expected)

    def test_roll_d6(self):
        expected = [6, 2, 2, 1, 5, 5, 6, 4, 5, 3]
        result = []
        for i in range(0, 10):
            roll = dice.roll_d6()
            result.append(roll)
        self.assertEqual(result, expected)

    def test_roll_d20(self):
        expected = [8, 5, 1, 18, 18, 13, 19, 10, 12, 7, 9, 12, 6, 8, 20, 8, 13, 17, 18, 8, 5]
        result = []
        for i in range(0, 21):
            roll = dice.roll_d20()
            result.append(roll)
        self.assertEqual(result, expected)
