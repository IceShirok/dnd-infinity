
from ddddd.entity import base


class Trait(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description


class LanguagesKnown(Trait):
    def __init__(self, languages):
        super(LanguagesKnown, self).__init__(name=base.LANGUAGES,
                                             description='these are the languages you know')
        self.languages = languages


class ProficiencyKnown(Trait):
    def __init__(self, name, proficiency_type, proficiencies):
        super(ProficiencyKnown, self).__init__(name=name,
                                               description='these are the things you''re proficient in')
        self.proficiency_type = proficiency_type
        self.proficiencies = proficiencies


class Darkvision(Trait):
    def __init__(self, range):
        super(Darkvision, self).__init__(name='Darkvision',
                                         description='Accustomed to life underground, you have superior vision in dark \
                                         and dim Conditions. You can see in dim light within 60 feet of you as if it \
                                         were bright light, and in Darkness as if it were dim light. You can''t \
                                         discern color in Darkness, only shades of gray.')
        self.range = range


class Toughness(Trait):
    def __init__(self, name):
        super(Toughness, self).__init__(name=name,
                                        description='Your hit point maximum increases by 1, \
                                               and it increases by 1 every time you gain a level.')
