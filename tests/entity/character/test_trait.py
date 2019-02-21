import unittest

from ddddd.entity import base
from ddddd.entity.character import trait


class TestTraitFunctions(unittest.TestCase):
    def test_format_list_as_english_string(self):
        self.assertEqual('', trait.format_list_as_english_string([]))
        self.assertEqual('Athletics',
                         trait.format_list_as_english_string(['athletics']))
        self.assertEqual('Athletics and Acrobatics',
                         trait.format_list_as_english_string(['athletics', 'acrobatics']))
        self.assertEqual('Athletics, Acrobatics, and Stealth',
                         trait.format_list_as_english_string(['athletics', 'acrobatics', 'stealth']))
