import unittest

from ddddd.entity import base
from ddddd.entity.character import race, trait


class TestRace(unittest.TestCase):
    def setUp(self):
        traits = [
            trait.Darkvision(range=60),
            trait.ToolProficiency(name='Tool Proficiency',
                                  proficiencies=['brewers_kit'])
        ]
        self.race = race.Race(name='race',
                              asi={},
                              size='medium',
                              speed=25,
                              languages=None,
                              traits=traits)

    def test_str_movement_multiplier(self):
        result = self.race.str_movement_multiplier
        self.assertEqual(result, 1)

    def test_skills(self):
        result = self.race.skills
        self.assertEqual(result, [])

    def test_proficiencies(self):
        result = self.race.proficiencies
        self.assertEqual(len(result), 1)

        prof_result = result.get('Tool Proficiency')
        self.assertTrue(isinstance(prof_result, trait.ToolProficiency))

    def test_verify(self):
        self.assertEqual(self.race.verify(), {})

    def test_required(self):
        self.assertEqual(self.race.required(), {})

###########################
# DWARF
###########################

class TestDwarfRace(unittest.TestCase):
    def setUp(self):
        tool_prof = [
            trait.ToolProficiency(name='Tool Proficiency',
                                  proficiencies=['brewers_kit'])
        ]
        self.dwarf = race.Dwarf(asi={},
                                traits=tool_prof)

    def test_default_traits(self):
        self.assertEqual(2, self.dwarf.asi['CON'].score_increase)

        expected_trait_names = {'Darkvision',
                                'Dwarven Combat Training',
                                'Dwarven Resilience',
                                'Stonecunning',
                                'Tool Proficiency'}

        result = set(map(lambda t: t.name, self.dwarf.traits))
        self.assertEqual(expected_trait_names, result)

        self.assertTrue(isinstance(self.dwarf.languages, trait.LanguagesKnown))

    def test_base_race(self):
        self.assertEqual(self.dwarf.base_race, 'Dwarf')

    def test_str_movement_multiplier(self):
        result = self.dwarf.str_movement_multiplier
        self.assertEqual(result, 1)

    def test_skills(self):
        result = self.dwarf.skills
        self.assertEqual(result, [])

    def test_proficiencies(self):
        prof = self.dwarf.proficiencies

        self.assertEqual(4, len(prof[base.WEAPON_PROFICIENCY].proficiencies))

        self.assertEqual('brewers_kit', prof[base.TOOL_PROFICIENCY].proficiencies[0])

    def test_required(self):
        req = self.dwarf.required()
        self.assertEqual(1, len(req.keys()))


class TestHillDwarfRace(unittest.TestCase):
    def setUp(self):
        tool_prof = [
            trait.ToolProficiency(name='Tool Proficiency',
                                  proficiencies=['brewers_kit'])
        ]
        self.hill_dwarf = race.HillDwarf(traits=tool_prof)

    def test_default_traits(self):
        self.assertEqual(2, self.hill_dwarf.asi['CON'].score_increase)
        self.assertEqual(1, self.hill_dwarf.asi['WIS'].score_increase)

        expected_trait_names = {'Darkvision',
                                'Dwarven Combat Training',
                                'Dwarven Resilience',
                                'Stonecunning',
                                'Tool Proficiency',
                                'Dwarven Toughness'}
        result = set(map(lambda t: t.name, self.hill_dwarf.traits))
        self.assertEqual(expected_trait_names, result)

    def test_base_race(self):
        self.assertEqual(self.hill_dwarf.base_race, 'Dwarf')

    def test_str_movement_multiplier(self):
        result = self.hill_dwarf.str_movement_multiplier
        self.assertEqual(result, 1)

    def test_skills(self):
        result = self.hill_dwarf.skills
        self.assertEqual(result, [])

    def test_proficiencies(self):
        prof = self.hill_dwarf.proficiencies

        self.assertEqual(4, len(prof[base.WEAPON_PROFICIENCY].proficiencies))

        self.assertEqual('brewers_kit', prof[base.TOOL_PROFICIENCY].proficiencies[0])


###########################
# GNOME
###########################

class TestGnomeRace(unittest.TestCase):
    def setUp(self):
        self.gnome = race.Gnome(asi={},
                                traits=[])

    def test_default_traits(self):
        self.assertEqual(2, self.gnome.asi['INT'].score_increase)

        expected_trait_names = {'Darkvision',
                                'Gnome Cunning'}

        result = set(map(lambda t: t.name, self.gnome.traits))
        self.assertEqual(expected_trait_names, result)

        self.assertTrue(isinstance(self.gnome.languages, trait.LanguagesKnown))

    def test_base_race(self):
        self.assertEqual(self.gnome.base_race, 'Gnome')

    def test_str_movement_multiplier(self):
        result = self.gnome.str_movement_multiplier
        self.assertEqual(result, 1)

    def test_skills(self):
        result = self.gnome.skills
        self.assertEqual(result, [])

    def test_proficiencies(self):
        self.assertEqual(len(self.gnome.proficiencies), 0)


class TestRockGnomeRace(unittest.TestCase):
    def setUp(self):
        self.rock_gnome = race.RockGnome()

    def test_default_traits(self):
        self.assertEqual(2, self.rock_gnome.asi['INT'].score_increase)
        self.assertEqual(1, self.rock_gnome.asi['CON'].score_increase)

        expected_trait_names = {'Darkvision',
                                'Gnome Cunning',
                                "Artificer's Lore",
                                'Tinker'}
        result = set(map(lambda t: t.name, self.rock_gnome.traits))
        self.assertEqual(expected_trait_names, result)

    def test_base_race(self):
        self.assertEqual(self.rock_gnome.base_race, 'Gnome')

    def test_str_movement_multiplier(self):
        result = self.rock_gnome.str_movement_multiplier
        self.assertEqual(result, 1)

    def test_skills(self):
        result = self.rock_gnome.skills
        self.assertEqual(result, [])

    def test_proficiencies(self):
        self.assertEqual(len(self.rock_gnome.proficiencies), 1)


###########################
# TIEFLING
###########################

class TestTieflingRace(unittest.TestCase):
    def setUp(self):
        self.tiefling = race.Tiefling()

    def test_default_traits(self):
        self.assertEqual(2, self.tiefling.asi['CHA'].score_increase)
        self.assertEqual(1, self.tiefling.asi['INT'].score_increase)

        expected_trait_names = {'Darkvision',
                                'Hellish Resistance',
                                'Infernal Legacy'}
        result = set(map(lambda t: t.name, self.tiefling.traits))
        self.assertEqual(expected_trait_names, result)

    def test_base_race(self):
        self.assertEqual(self.tiefling.base_race, 'Tiefling')

    def test_str_movement_multiplier(self):
        result = self.tiefling.str_movement_multiplier
        self.assertEqual(result, 1)

    def test_skills(self):
        result = self.tiefling.skills
        self.assertEqual(result, [])

    def test_proficiencies(self):
        self.assertEqual(len(self.tiefling.proficiencies), 0)


###########################
# DRAGONBORN
###########################

class TestDragonbornRace(unittest.TestCase):
    def setUp(self):
        self.dragonborn = race.Dragonborn('bronze')

    def test_default_traits(self):
        self.assertEqual(2, self.dragonborn.asi['STR'].score_increase)
        self.assertEqual(1, self.dragonborn.asi['CHA'].score_increase)

        expected_trait_names = {'Draconic Ancestry',
                                'Damage Resistance',
                                'Breath Weapon'}
        result = set(map(lambda t: t.name, self.dragonborn.traits))
        self.assertEqual(expected_trait_names, result)

    def test_race(self):
        self.assertEqual(self.dragonborn.name, 'Bronze Dragonborn')

    def test_base_race(self):
        self.assertEqual(self.dragonborn.base_race, 'Dragonborn')

    def test_str_movement_multiplier(self):
        result = self.dragonborn.str_movement_multiplier
        self.assertEqual(result, 1)

    def test_skills(self):
        result = self.dragonborn.skills
        self.assertEqual(result, [])

    def test_proficiencies(self):
        self.assertEqual(len(self.dragonborn.proficiencies), 0)

