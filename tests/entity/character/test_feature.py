import unittest

from ddddd.entity.character import feature


class TestTraitFunctions(unittest.TestCase):
    def test_format_list_as_english_string(self):
        self.assertEqual('', feature.format_list_as_english_string([]))
        self.assertEqual('Athletics',
                         feature.format_list_as_english_string(['athletics']))
        self.assertEqual('Athletics and Acrobatics',
                         feature.format_list_as_english_string(['athletics', 'acrobatics']))
        self.assertEqual('Athletics, Acrobatics, and Stealth',
                         feature.format_list_as_english_string(['athletics', 'acrobatics', 'stealth']))
