import unittest
from ddddd.entity.character import race


class TestRace(unittest.TestCase):
    def setUp(self):
        self.dorian = race.Race(name='race',
                                asi={},
                                size='medium',
                                speed=25,
                                languages=None,
                                traits=None)

    def test_str_movement_multiplier(self):
        result = self.dorian.str_movement_multiplier
        self.assertEqual(result, 1)


class TestDwarfRace(unittest.TestCase):
    def setUp(self):
        self.dorian = race.Dwarf(asi={},
                                 traits={'tool_proficiency': {'tools': ['brewers_kit']}})

    def test_default_traits(self):
        self.assertEqual({'CON': 2}, self.dorian.asi)
        self.assertEqual({'darkvision',
                          'dwarven_resilience',
                          'dwarven_combat_training',
                          'stonecunning',
                          'tool_proficiency',
                          'size'},
                         set(self.dorian.traits.keys()))

    def test_proficiencies(self):
        prof = self.dorian.proficiencies
        self.assertEqual(4, len(prof['weapons']))
        self.assertEqual('brewers_kit', prof['tools'][0])

    def test_required(self):
        req = self.dorian.required()
        self.assertEqual(1, len(req.keys()))

    def test_verify_good(self):
        self.assertEqual(True, self.dorian.verify())

    def test_verify_bad(self):
        no_tool = race.Dwarf(asi={}, traits=None)
        self.assertRaises(ValueError, no_tool.verify)

        invalid_tool = race.Dwarf(asi={}, traits={'tool_proficiency': {'tools': []}})
        self.assertRaises(ValueError, invalid_tool.verify)


class TestHillDwarfRace(unittest.TestCase):
    def setUp(self):
        self.dorian = race.HillDwarf(traits={'tool_proficiency': {'tools': ['brewers_kit']}})

    def test_default_traits(self):
        self.assertEqual({'CON': 2, 'WIS': 1}, self.dorian.asi)
        self.assertEqual({'darkvision',
                          'dwarven_resilience',
                          'dwarven_combat_training',
                          'stonecunning',
                          'tool_proficiency',
                          'size',
                          'dwarven_toughness'},
                         set(self.dorian.traits.keys()))
