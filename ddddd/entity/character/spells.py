
import json

from ddddd.entity import ability_score
from ddddd.entity.character import pc


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
            # 'level': self.level,
            # 'magic_school': self.magic_school,
            # 'casting_time': self.casting_time,
            # 'range': self.spell_range,
            # 'components': self.components,
            # 'duration': self.duration,
            # 'description': self.description,
        }

    def __str__(self):
        return json.dumps(self.__json__(), indent=4)


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

COMMAND = Spell(name='Command',
                level=1,
                magic_school='enchantment',
                casting_time='1 action',
                spell_range='60ft',
                components=['verbal'],
                duration='1 round',
                description='You speak a one-word command to a creature you can see within range.')


SPELLCASTING_ABILITY = 'spellcasting_ability'
LIST_SPELLS_KNOWN = 'list_spells_known'
SPELL_SLOTS = 'spell_slots'

MODIFIER = 'modifier'

CANTRIPS = 'cantrips'
FIRST = '1st'
SECOND = '2nd'
THIRD = '3rd'
FOURTH = '4th'
FIFTH = '5th'
SIXTH = '6th'
SEVENTH = '7th'
EIGHTH = '8th'
NINTH = '9th'
ORD_TO_NUM = {
    CANTRIPS: 0, FIRST: 1, SECOND: 2, THIRD: 3, FOURTH: 4,
    FIFTH: 5, SIXTH: 6, SEVENTH: 7, EIGHTH: 8, NINTH: 9,
}
NUM_TO_ORD = {
    0: CANTRIPS, 1: FIRST, 2: SECOND, 3: THIRD, 4: FOURTH,
    5: FIFTH, 6: SIXTH, 7: SEVENTH, 8: EIGHTH, 9: NINTH,
}


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
        self._verify()

    def spell_save_dc(self, ability_scores, proficiency_bonus):
        return 8 + ability_scores[self.spellcasting_ability][MODIFIER] + proficiency_bonus

    def spell_attack_bonus(self, ability_scores, proficiency_bonus):
        return ability_scores[self.spellcasting_ability][MODIFIER] + proficiency_bonus

    def _verify(self):
        cantrips = list(filter(lambda x: x.level == 0, self.list_spells_known))
        num_cantrips_know = self.spell_slots[CANTRIPS]
        if len(cantrips) != num_cantrips_know:
            raise ValueError('Must have {} cantrips but inputted {} cantrips!'.format(num_cantrips_know, len(cantrips)))

        spells = list(filter(lambda x: x.level > 0, self.list_spells_known))
        for s in spells:
            if NUM_TO_ORD[s.level] not in self.spell_slots:
                raise ValueError('Cannot cast a {}-level spell - you don''t have the spell slots for it!'.format(NUM_TO_ORD[s.level]))

    def __json__(self):
        spells_p = {}
        for s in self.list_spells_known:
            lvl_ord = NUM_TO_ORD[s.level]
            if lvl_ord in spells_p:
                spells_p[lvl_ord].append(s.__json__())
            else:
                spells_p[lvl_ord] = [s.__json__()]

        return {
            SPELLCASTING_ABILITY: self.spellcasting_ability,
            LIST_SPELLS_KNOWN: spells_p,
            SPELL_SLOTS: self.spell_slots,
        }

    def __str__(self):
        return json.dumps(self.__json__(), indent=4)


def test_spells():
    ability_scores = {'WIS': {'modifier': 5}}
    proficiency_bonus = 3
    spell_slots = {
        CANTRIPS: 4,
        FIRST: 4,
        SECOND: 3,
        THIRD: 3,
        FOURTH: 2,
    }
    list_spells = []
    simple_spell_list = [
        ('Sacred Flame', 0),
        ('Guidance', 0),
        ('Mending', 0),
        ('Word of Radiance', 0),
        ('Command', 1),
        ('Identify', 1),
        ('Bless', 1),
        ('Healing Word', 1),
        ('Guiding Bolt', 1),
        ('Augury', 2),
        ('Suggestion', 2),
        ('Spiritual Weapon', 2),
        ('Enhance Ability', 2),
        ('Nondetection', 3),
        ('Speak with Dead', 3),
        ('Beacon of Hope', 3),
        ('Spirit Guardians', 3),
        ('Arcane Eye', 4),
        ('Confusion', 4),
        ('Freedom of Movement', 4),
        ('Banishment', 4),
    ]
    for name, level in simple_spell_list:
        list_spells.append(Spell(name=name, level=level,
                                 magic_school='',
                                 casting_time='',
                                 spell_range='',
                                 components=['verbal', 'somatic'],
                                 duration='',
                                 description=''))
    spellcasting_ability = SpellcastingAbility(spellcasting_ability=ability_score.WIS,
                                               spell_slots=spell_slots,
                                               list_spells_known=list_spells)
    print(spellcasting_ability)
    print('Spell save DC: {}'.format(spellcasting_ability.spell_save_dc(ability_scores, proficiency_bonus)))
    print('Spell attack bonus: {}'.format(spellcasting_ability.spell_attack_bonus(ability_scores, proficiency_bonus)))


if __name__ == '__main__':
    test_spells()
