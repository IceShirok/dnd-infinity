
class Spell(object):
    """
    A singular spell in D&D.
    I will very likely keep the majority of the information in a database
    because of the sheer number of spells in the book. Some spells will
    be manually created into objects for testing purposes.
    """
    def __init__(self, name, level, magic_school,
                 casting_time, spell_range, components, duration,
                 description):
        self.name = name
        self.level = level
        self.magic_school = magic_school
        self.casting_time = casting_time
        self.spell_range = spell_range
        self.components = components
        self.duration = duration
        self.description = description
    
    def __json__(self):
        return {
            'spell': self.name,
            'level': self.level,
            'magic_school': self.magic_school,
            'casting_time': self.casting_time,
            'range': self.spell_range,
            'components': self.components,
            'duration': self.duration,
            'description': self.description,
        }


# Cantrips (level 0 spells)
CHILL_TOUCH = Spell(name='Chill Touch',
                    level=0,
                    magic_school='necromancy',
                    casting_time='1 action',
                    spell_range='120ft',
                    components=['verbal', 'somatic'],
                    duration='1 round',
                    description='You create a ghostly, skeletal hand in the space of a creature within range.')

# 1st level spells
BLESS = Spell(name='Bless',
              level=1,
              magic_school='enchantment',
              casting_time='1 action',
              spell_range='30ft',
              components=['verbal', 'somatic', 'material (a sprinking of holy water)'],
              duration='concentration, up to 1 minute',
              description='You bless up to three creatures of your choice within range.')


class SpellcastingAbility(object):
    """
    An object representing a character's ability to cast spells.
    This is likely going to be delegated to the class factory, as each class
    will known the number of spells and the available spell slots
    for that class and level. I'm not sure whether to add the spellcasting
    bonus and DCs here or at the class level...
    """
    def __init__(self, list_spells_known, spell_slots):
        self.list_spells_known = list_spells_known
        self.spell_slots = spell_slots

    def __json__(self):
        return {
            'list_spells_known': self.list_spells_known,
            'spell_slots': self.spell_slots,
        }
