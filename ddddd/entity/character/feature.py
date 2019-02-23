from ddddd.entity.character import base


class Feature(object):
    """
    This is the representation of a "trait" or "feature" for a player character (PC).
    Features comprise of a name and description, and optionally a list of specific
    tidbits (i.e. favored enemies) and/or functionality (toughness -> more HP).

    For the sake of DDD, I chose the name "feature" over "trait" because more
    modules refer these types of "miscellaneous flairs for a PC" as a "feature"
    (from vocation and background) than a "trait" (race). This may get slightly
    confusing as "feats" are a subset of "features".

    Features <- racial "traits", vocation "features", background "feature", "feats"

    Features are considered immutable, so aggregating traits must result in a new
    trait object.
    """
    def __init__(self, name, description):
        self.name = name
        self.description = description


def format_list_as_english_string(a_list):
    capped_list = list(map(lambda x: x.capitalize(), a_list))
    if len(capped_list) == 0:
        return ''
    elif len(capped_list) == 1:
        return capped_list[0]
    elif len(capped_list) == 2:
        return '{} and {}'.format(capped_list[0], capped_list[1])
    else:
        last_item = ', and {}'.format(capped_list[-1])
        return ', '.join(capped_list[:-1]) + last_item


class LanguagesKnown(Feature):
    def __init__(self, languages, name=None, description=None):
        name = name if name else base.LANGUAGES
        self.languages = languages
        flavor = '{} '.format(description) if description else ''
        final_desc = '{}You know {}.'.format(flavor, format_list_as_english_string(languages))
        super(LanguagesKnown, self).__init__(name=name,
                                             description=final_desc)


class ProficiencyKnown(Feature):
    def __init__(self, name, proficiencies, proficiency_type, description=None):
        description = description if description else 'these are the things you''re proficient in'
        super(ProficiencyKnown, self).__init__(name=name,
                                               description=description)
        self.proficiencies = proficiencies
        self.proficiency_type = proficiency_type


class ArmorProficiency(ProficiencyKnown):
    def __init__(self, proficiencies, name=None, description=None):
        description = description if description else 'You gain proficiency with {} armor.'.format(format_list_as_english_string(proficiencies))
        super(ArmorProficiency, self).__init__(name=name if name else 'Armor Proficiency',
                                               description=description,
                                               proficiencies=proficiencies,
                                               proficiency_type='Armor Proficiency')


class WeaponProficiency(ProficiencyKnown):
    def __init__(self, proficiencies, name=None, description=None):
        description = description if description else 'You gain proficiency with the {}.'.format(format_list_as_english_string(proficiencies))
        super(WeaponProficiency, self).__init__(name=name if name else 'Weapon Proficiency',
                                                description=description,
                                                proficiencies=proficiencies,
                                                proficiency_type='Weapon Proficiency')


class ToolProficiency(ProficiencyKnown):
    def __init__(self, proficiencies, name=None, description=None):
        description = description if description else 'You gain proficiency with {}.'.format(format_list_as_english_string(proficiencies))
        super(ToolProficiency, self).__init__(name=name if name else 'Tool Proficiency',
                                              description=description,
                                              proficiencies=proficiencies,
                                              proficiency_type='Tool Proficiency')


class Darkvision(Feature):
    def __init__(self, range):
        super(Darkvision, self).__init__(name='Darkvision',
                                         description='Accustomed to life underground, you have superior vision in dark \
                                         and dim Conditions. You can see in dim light within {} feet of you as if it \
                                         were bright light, and in Darkness as if it were dim light. You can''t \
                                         discern color in Darkness, only shades of gray.'.format(range))
        self.range = range


class Toughness(Feature):
    def __init__(self, name):
        super(Toughness, self).__init__(name=name,
                                        description='Your hit point maximum increases by 1, \
                                                     and it increases by 1 every time you gain a level.')


class Expertise(Feature):
    def __init__(self, skills, proficiencies, name=None, description=None):
        self.skills = skills if skills else []
        self.proficiencies = proficiencies if proficiencies else []
        flavor = '{} '.format(description) if description else 'Your Proficiency Bonus is doubled for any ability check \
                                                                you make that uses the chosen proficiencies. '
        final_desc = '{}You have expertise in {}.'.format(flavor, format_list_as_english_string(self.skills + self.proficiencies))
        super(Expertise, self).__init__(name=name if name else 'Expertise',
                                        description=final_desc)


class EnhanceDamage(Feature):
    def __init__(self, name, description, attack_bonus):
        super(EnhanceDamage, self).__init__(name, description)
        self.attack_bonus = attack_bonus

    def qualifies(self, weapon):
        """Checks to see whether this weapon is qualified for the attack bonus"""
        return True


class DamageResistance(Feature):
    def __init__(self, damage_type, name=None, description=None):
        name = name if name else 'Damage Resistance'
        description = description if description else 'You have Resistance with {} damage.'.format(damage_type)
        super(DamageResistance, self).__init__(name, description)
        self.resistance = damage_type


# TODO refactor this into a feat later
# for now, feats can be treated like traits
class WarCaster(Feature):
    def __init__(self):
        super(WarCaster, self).__init__(name='War Caster',
                                        description='You have advantage one Constitution saves \
                                        that you make to maintain concentration on a spell when you take damage.')
