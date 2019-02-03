
import json

from ddddd.entity import base

class SpellcastingAbility(object):
    """
    An object representing a character's ability to cast spells.
    This is likely going to be delegated to the class factory, as each class
    will known the number of spells and the available spell slots
    for that class and level. I'm not sure whether to add the spellcasting
    bonus and DCs here or at the class level...
    """
    def __init__(self, spellcasting_ability, spell_slots, list_spells_known):
        self.spellcasting_ability = spellcasting_ability
        self.spell_slots = spell_slots
        self.list_spells_known = list_spells_known

    def spell_save_dc(self, ability_scores, proficiency_bonus):
        return 8 + ability_scores[self.spellcasting_ability].modifier + proficiency_bonus

    def spell_attack_bonus(self, ability_scores, proficiency_bonus):
        return ability_scores[self.spellcasting_ability].modifier + proficiency_bonus

    def _verify(self):
        cantrips = list(filter(lambda x: x.level == 0, self.list_spells_known))
        if len(cantrips) > 0:
            if base.SpellTypes.CANTRIPS not in self.spell_slots:
                raise ValueError('Cannot learn cantrips!')
            num_cantrips_know = self.spell_slots[base.SpellTypes.CANTRIPS]
            if len(cantrips) != num_cantrips_know:
                raise ValueError('Must have {} cantrips but inputted {} cantrips!'.format(num_cantrips_know, len(cantrips)))

        spells = list(filter(lambda x: x.level != base.SpellTypes.CANTRIPS, self.list_spells_known))
        for s in spells:
            if s.level not in self.spell_slots:
                raise ValueError('Cannot cast a {}-level spell - you don''t have the spell slots for it!'.format(s.level))


def generate_simple_spell(name, level):
    return Spell(name=name, level=level,
                 magic_school='enchantment',
                 casting_time='1 action',
                 spell_range='30 ft',
                 components=['verbal', 'somatic'],
                 duration='instantaneous',
                 description='This is a spell.')


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


# Cantrips (level 0 spells)
CHILL_TOUCH = Spell(name='Chill Touch',
                    level=base.SpellTypes.CANTRIPS,
                    magic_school='necromancy',
                    casting_time='1 action',
                    spell_range='120ft',
                    components=['verbal', 'somatic'],
                    duration='1 round',
                    description='You create a ghostly, skeletal hand in the space of a creature within range.')

# 1st level spells
BLESS = Spell(name='Bless',
              level=base.SpellTypes.FIRST,
              magic_school='enchantment',
              casting_time='1 action',
              spell_range='30ft',
              components=['verbal', 'somatic', 'material (a sprinking of holy water)'],
              duration='concentration, up to 1 minute',
              description='You bless up to three creatures of your choice within range.')

COMMAND = Spell(name='Command',
                level=base.SpellTypes.FIRST,
                magic_school='enchantment',
                casting_time='1 action',
                spell_range='60ft',
                components=['verbal'],
                duration='1 round',
                description='You speak a one-word command to a creature you can see within range.')
