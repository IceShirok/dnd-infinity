import unittest
from ddddd.entity import base


class TestFunctions(unittest.TestCase):
    def test_modifier(self):
        # test most extreme modifiers
        self.assertEqual(base.modifier(1), -5)
        self.assertEqual(base.modifier(20), 5)

        # test that the modifier changes correctly
        self.assertEqual(base.modifier(7), -2)
        self.assertEqual(base.modifier(8), -1)
        self.assertEqual(base.modifier(9), -1)
        self.assertEqual(base.modifier(10), 0)
        self.assertEqual(base.modifier(11), 0)
        self.assertEqual(base.modifier(12), 1)
        self.assertEqual(base.modifier(13), 1)

    def test_prettify_modifier(self):
        self.assertEqual(base.prettify_modifier(-1), '-1')
        self.assertEqual(base.prettify_modifier(0), '0')
        self.assertEqual(base.prettify_modifier(1), '+1')
