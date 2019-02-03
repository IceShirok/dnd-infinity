import unittest

from ddddd.entity import base
from ddddd.entity.character import race, trait


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
        tool_prof = [
            trait.ToolProficiency(name='Tool Proficiency',
                                  proficiencies=['brewers_kit'])
        ]
        self.dorian = race.Dwarf(asi={},
                                 traits=tool_prof)

    def test_default_traits(self):
        self.assertEqual(2, self.dorian.asi['CON'].score_increase)

        expected_trait_names = {'Darkvision',
                                'Dwarven Combat Training',
                                'Dwarven Resilience',
                                'Stonecunning',
                                'Tool Proficiency'}
        result = set(map(lambda t: t.name, self.dorian.traits))
        self.assertEqual(expected_trait_names, result)

    def test_proficiencies(self):
        prof = self.dorian.proficiencies

        self.assertEqual(4, len(prof[base.WEAPON_PROFICIENCY].proficiencies))

        tool_prof = list(filter(lambda p: isinstance(p, trait.ToolProficiency), prof))
        self.assertEqual('brewers_kit', prof[base.TOOL_PROFICIENCY].proficiencies[0])

    def test_required(self):
        req = self.dorian.required()
        self.assertEqual(1, len(req.keys()))

    def test_verify_good(self):
        self.assertEqual({}, self.dorian.verify())

    # def test_verify_bad(self):
    #     no_tool = race.Dwarf(asi={}, traits=None)
    #     self.assertRaises(ValueError, no_tool.verify)
    #
    #     invalid_tool = race.Dwarf(asi={}, traits={'tool_proficiency': {'tools': []}})
    #     self.assertRaises(ValueError, invalid_tool.verify)


class TestHillDwarfRace(unittest.TestCase):
    def setUp(self):
        tool_prof = [
            trait.ToolProficiency(name='Tool Proficiency',
                                  proficiencies=['brewers_kit'])
        ]
        self.dorian = race.HillDwarf(traits=tool_prof)

    def test_default_traits(self):
        self.assertEqual(2, self.dorian.asi['CON'].score_increase)
        self.assertEqual(1, self.dorian.asi['WIS'].score_increase)

        expected_trait_names = {'Darkvision',
                                'Dwarven Combat Training',
                                'Dwarven Resilience',
                                'Stonecunning',
                                'Tool Proficiency',
                                'Dwarven Toughness'}
        result = set(map(lambda t: t.name, self.dorian.traits))
        self.assertEqual(expected_trait_names, result)
