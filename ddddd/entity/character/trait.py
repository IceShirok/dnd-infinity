
from ddddd.entity import base


class Trait(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description


class LanguagesKnown(Trait):
    def __init__(self, languages, name=None, description=None):
        name = name if name else base.LANGUAGES
        description = description if description else 'these are the languages you know'
        super(LanguagesKnown, self).__init__(name=name,
                                             description=description)
        self.languages = languages


class ProficiencyKnown(Trait):
    def __init__(self, name, proficiencies, proficiency_type, description=None):
        description = description if description else 'these are the things you''re proficient in'
        super(ProficiencyKnown, self).__init__(name=name,
                                               description=description)
        self.proficiencies = proficiencies
        self.proficiency_type = proficiency_type


class ArmorProficiency(ProficiencyKnown):
    def __init__(self, proficiencies, name=None, description=None):
        description = description if description else 'You gain proficiency with a type of armor.'
        super(ArmorProficiency, self).__init__(name=name if name else 'Armor Proficiency',
                                               description=description,
                                               proficiencies=proficiencies,
                                               proficiency_type='Armor Proficiency')


class WeaponProficiency(ProficiencyKnown):
    def __init__(self, proficiencies, name=None, description=None):
        description = description if description else 'You gain proficiency with a weapon.'
        super(WeaponProficiency, self).__init__(name=name if name else 'Weapon Proficiency',
                                                description=description,
                                                proficiencies=proficiencies,
                                                proficiency_type='Weapon Proficiency')


class ToolProficiency(ProficiencyKnown):
    def __init__(self, proficiencies, name=None, description=None):
        description = description if description else 'You gain proficiency with a tool.'
        super(ToolProficiency, self).__init__(name=name if name else 'Tool Proficiency',
                                              description=description,
                                              proficiencies=proficiencies,
                                              proficiency_type='Tool Proficiency')


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


class Expertise(Trait):
    def __init__(self, skills, proficiencies, name=None, description=None):
        description = description if description else 'Your Proficiency Bonus is doubled for any ability check \
                                        you make that uses the chosen proficiencies.'
        super(Expertise, self).__init__(name=name if name else 'Expertise',
                                        description=description)
        self.skills = skills if skills else []
        self.proficiencies = proficiencies if proficiencies else []


class EnhanceWeaponAttack(Trait):
    def __init__(self, name, description, attack_bonus):
        super(EnhanceWeaponAttack, self).__init__(name, description)
        self.attack_bonus = attack_bonus

    def qualifies(self, weapon):
        """Checks to see whether this weapon is qualified for the attack bonus"""
        return True
