import unittest
from ddddd.entity.character import background, trait


class TestBackground(unittest.TestCase):
    def setUp(self):
        prof = {
            'skills': ['stealth', 'deception'],
            'Tool Proficiency': trait.ToolProficiency(proficiencies=['thieves_tools', 'bone_dice']),
            'Weapon Proficiency': trait.WeaponProficiency(proficiencies=['warhammer']),
            'Armor Proficiency': trait.ArmorProficiency(proficiencies=['light']),
        }
        lang = trait.LanguagesKnown(languages=['Elvish'])
        self.bg = background.Background(name='background',
                                        feature=trait.Trait(name='Trait', description=''),
                                        proficiencies=prof,
                                        languages=lang)

    def test_feature(self):
        result = self.bg.feature
        self.assertTrue(isinstance(result, trait.Trait))

    def test_all_proficiencies(self):
        prof = self.bg.background_proficiencies
        self.assertEqual(4, len(prof.keys()))

    def test_skills(self):
        skills = self.bg.skills
        self.assertEqual(['stealth', 'deception'], skills)

    def test_nonskill_proficiencies(self):
        prof = self.bg.proficiencies
        self.assertEqual(3, len(prof.keys()))
        self.assertTrue('skills' not in prof.keys())


class TestCriminalBackground(unittest.TestCase):
    def setUp(self):
        self.criminal = background.Criminal()

    def test_feature(self):
        result = self.criminal.feature
        self.assertTrue(isinstance(result, trait.Trait))

    def test_all_proficiencies(self):
        prof = self.criminal.background_proficiencies
        self.assertEqual(2, len(prof.keys()))

    def test_skills(self):
        skills = self.criminal.skills
        self.assertEqual(2, len(skills))


class TestNobleBackground(unittest.TestCase):
    def setUp(self):
        tool = trait.ToolProficiency(proficiencies=['chess_set'])
        lang = trait.LanguagesKnown(languages=['elvish', 'dwarvish'])
        self.noble = background.Noble(tool_proficiency=tool, languages=lang)

    def test_feature(self):
        result = self.noble.feature
        self.assertTrue(isinstance(result, trait.Trait))

    def test_all_proficiencies(self):
        prof = self.noble.background_proficiencies
        self.assertEqual(2, len(prof.keys()))

    def test_skills(self):
        skills = self.noble.skills
        self.assertEqual(2, len(skills))


class TestSageBackground(unittest.TestCase):
    def setUp(self):
        lang = trait.LanguagesKnown(languages=['elvish', 'dwarvish'])
        self.sage = background.Sage(languages=lang)

    def test_feature(self):
        result = self.sage.feature
        self.assertTrue(isinstance(result, trait.Trait))

    def test_all_proficiencies(self):
        prof = self.sage.background_proficiencies
        self.assertEqual(1, len(prof.keys()))

    def test_skills(self):
        skills = self.sage.skills
        self.assertEqual(2, len(skills))

