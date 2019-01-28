import unittest
from ddddd.entity.character import background


class TestBackground(unittest.TestCase):
    def setUp(self):
        self.dorian = background.PlayerBackground(name='background',
                                                  feature=None,
                                                  proficiencies={'skills': ['history'], 'tools': ['chess_set']},
                                                  languages=['elvish'])

    def test_all_proficiencies(self):
        prof = self.dorian.background_proficiencies
        self.assertEqual(2, len(prof.keys()))

    def test_skills(self):
        skills = self.dorian.skills
        self.assertEqual(1, len(skills))

    def test_nonskill_proficiencies(self):
        prof = self.dorian.proficiencies
        self.assertTrue('tools' in prof.keys())
        self.assertTrue('skills' not in prof.keys())


class TestCriminalBackground(unittest.TestCase):
    def setUp(self):
        self.dorian = background.Criminal()

    def test_all_proficiencies(self):
        prof = self.dorian.background_proficiencies
        self.assertEqual(2, len(prof.keys()))

    def test_skills(self):
        skills = self.dorian.skills
        self.assertEqual(2, len(skills))
