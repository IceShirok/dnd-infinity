from ddddd.entity.character import base
from ddddd.entity.character.base import SpellTypes


class SpellcastingAbility(object):
    """
    An object representing a character's ability to cast spells.
    This is likely going to be delegated to the class factory, as each class
    will known the number of spells and the available spell slots
    for that class and level. I'm not sure whether to add the spellcasting
    bonus and DCs here or at the class level...
    """
    def __init__(self, spellcasting_ability,
                 spell_slots, casting_spells,
                 num_cantrips_known=0, cantrips=None):
        self.spellcasting_ability = spellcasting_ability

        self.spell_slots = spell_slots
        self.casting_spells = casting_spells

        self.num_cantrips_known = num_cantrips_known
        self.cantrips = cantrips if cantrips else []

    def spell_save_dc(self, ability_scores, proficiency_bonus):
        return 8 + ability_scores[self.spellcasting_ability].modifier + proficiency_bonus

    def spell_attack_bonus(self, ability_scores, proficiency_bonus):
        return ability_scores[self.spellcasting_ability].modifier + proficiency_bonus

    def _verify(self):
        if len(self.cantrips) > 0:
            if self.num_cantrips_known > 0:
                raise ValueError('Cannot learn cantrips!')
            if len(self.cantrips) != self.num_cantrips_known:
                raise ValueError('Must have {} cantrips but inputted {} cantrips!'.format(self.num_cantrips_known,
                                                                                          len(self.cantrips)))

        for s in self.casting_spells:
            if s.level not in self.spell_slots:
                raise ValueError('Cannot cast a {}-level spell - you don''t have the spell slots for it!'.format(s.level))


def generate_simple_spell_list(spell_list):
    """
    Generates a quick spell list from a list of spell name/level pair.
    :param spell_list: a list of spell name/level tuples.
    :return: a list of spells with default params.
    """
    return list(map(lambda s: generate_simple_spell(s[0], s[1]), spell_list))


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


class Cantrip(Spell):
    """
    A cantrip is a spell that can be cast at will, without using a spell slot
    and without being prepared in advance. Repeated practice has fixed the spell
    in the caster's mind and infused the caster with the magic needed to produce
    the effect over and over. A cantrip's spell level is 0.

    A cantrip is its separate class because a cantrip is not exhausted like
    a spell slot. It's better to say that it could be treated as a weapon.
    """

    def __init__(self, name, magic_school,
                 casting_time, spell_range, components, duration,
                 description):
        super(Cantrip, self).__init__(name=name,
                                      level='cantrip',
                                      magic_school=magic_school,
                                      casting_time=casting_time,
                                      spell_range=spell_range,
                                      components=components,
                                      duration=duration,
                                      description=description)


class DamageCantrip(Cantrip):
    """
    A damage cantrip is a cantrip that would act as the spellcaster's
    magical weapon. This cantrip is able to spit out the calculations
    for attack bonuses/spell save DC and damage like a weapon.
    """
    def __init__(self, name, magic_school,
                 casting_time, spell_range, components, duration,
                 description, attack_bonus_calc, damage_calc):
        super(DamageCantrip, self).__init__(name=name,
                                            magic_school=magic_school,
                                            casting_time=casting_time,
                                            spell_range=spell_range,
                                            components=components,
                                            duration=duration,
                                            description=description)
        self.attack_bonus_calc = attack_bonus_calc
        self.damage_calc = damage_calc

    def calculate_attack_bonus(self, spell_attack_bonus, spell_save_dc):
        return self.attack_bonus_calc(spell_attack_bonus, spell_save_dc)

    def calculate_damage_calc(self, caster_level):
        return self.damage_calc(caster_level)


##############################
# CANTRIPS
##############################

# Some classes may follow this pattern
def cantrips_by_level(level):
    if level < 4:
        return 3
    elif level < 10:
        return 4
    else:
        return 5


def spell_dc_with_ability(ability):
    def spell_dc(_, spell_save_dc):
        return '{} DC {}'.format(ability, spell_save_dc)
    return spell_dc


def spell_attack(spell_attack_bonus, _):
    return '{}'.format(spell_attack_bonus)


def damage_by_level_with_dice(dice_format):
    def damage_by_level(caster_level):
        if caster_level < 5:
            num_dice = 1
        elif caster_level < 11:
            num_dice = 2
        elif caster_level < 17:
            num_dice = 3
        else:
            num_dice = 4
        return dice_format.format(num_dice)
    return damage_by_level


SACRED_FLAME = DamageCantrip(name='Sacred Flame',
                             magic_school='evocation',
                             casting_time='1 action',
                             spell_range=60,
                             components=['verbal', 'somatic'],
                             duration='instantaneous',
                             description='Flame-like radiance descends on a creature that you can see within range.',
                             attack_bonus_calc=spell_dc_with_ability(base.AbilityScore.DEX),
                             damage_calc=damage_by_level_with_dice('{}d8 fire'))

GUIDANCE = Cantrip(name='Guidance',
                   magic_school='divination',
                   casting_time='1 action',
                   spell_range='touch',
                   components=['verbal', 'somatic'],
                   duration='concentration, up to 1 minute',
                   description='Once before the spell ends, the target can roll a d4 \
                   and add the number rolled to one ability check of its choice.')

SPARE_THE_DYING = Cantrip(name='Spare the Dying',
                          magic_school='necromancy',
                          casting_time='1 action',
                          spell_range='touch',
                          components=['verbal', 'somatic'],
                          duration='instantaneous',
                          description='You touch a living creature that has 0 hit points. \
                          The creature becomes stable. \
                          This spell has no effect on undead or constructs.')

WORD_OF_RADIANCE = DamageCantrip(name='Word of Radiance',
                                 magic_school='evocation',
                                 casting_time='1 action',
                                 spell_range='5 ft',
                                 components=['verbal', 'material (a holy symbol)'],
                                 duration='instantaneous',
                                 description='You utter a divine word, and burning radiance erupts from you. \
                                    Each creature of your choice that you can see within range must succeed on a \
                                    Constitution saving throw or take Xd6 radiant damage.',
                                 attack_bonus_calc=spell_dc_with_ability(base.AbilityScore.CON),
                                 damage_calc=damage_by_level_with_dice('{}d6 radiant'))

MENDING = Cantrip(name='Mending',
                  magic_school='transmutation',
                  casting_time='1 action',
                  spell_range='touch',
                  components=['verbal', 'somatic'],
                  duration='instantaneous',
                  description='')


##############################
# SPELLS
##############################

# Most pure spellcasting classes will follow this pattern
def get_spell_slot_by_level(level):
    spell_slots = {
        SpellTypes.FIRST: 2
    }
    if level >= 2:
        spell_slots[SpellTypes.FIRST] = 3
    if level >= 3:
        spell_slots[SpellTypes.FIRST] = 4
        spell_slots[SpellTypes.SECOND] = 2
    if level >= 4:
        spell_slots[SpellTypes.SECOND] = 3
    if level >= 5:
        spell_slots[SpellTypes.SECOND] = 4
        spell_slots[SpellTypes.THIRD] = 2
    if level >= 6:
        spell_slots[SpellTypes.THIRD] = 3
    if level >= 7:
        spell_slots[SpellTypes.FOURTH] = 1
    if level >= 8:
        spell_slots[SpellTypes.FOURTH] = 2
    if level >= 9:
        spell_slots[SpellTypes.FOURTH] = 3
        spell_slots[SpellTypes.FIFTH] = 1
    if level >= 10:
        spell_slots[SpellTypes.FIFTH] = 1
    if level >= 11:
        spell_slots[SpellTypes.SIXTH] = 1
    if level >= 12:
        spell_slots[SpellTypes.SIXTH] = 1
    if level >= 13:
        spell_slots[SpellTypes.SEVENTH] = 1
    if level >= 14:
        spell_slots[SpellTypes.SEVENTH] = 1
    if level >= 15:
        spell_slots[SpellTypes.EIGHTH] = 1
    if level >= 16:
        spell_slots[SpellTypes.EIGHTH] = 1
    if level >= 17:
        spell_slots[SpellTypes.NINTH] = 1
    if level >= 18:
        spell_slots[SpellTypes.FIFTH] = 2
    if level >= 19:
        spell_slots[SpellTypes.SIXTH] = 2
    if level >= 20:
        spell_slots[SpellTypes.SEVENTH] = 2
    return spell_slots


# 1st level spells
BLESS = Spell(name='Bless',
              level=SpellTypes.FIRST,
              magic_school='enchantment',
              casting_time='1 action',
              spell_range='30ft',
              components=['verbal', 'somatic', 'material (a sprinking of holy water)'],
              duration='concentration, up to 1 minute',
              description='You bless up to three creatures of your choice within range.')

COMMAND = Spell(name='Command',
                level=SpellTypes.FIRST,
                magic_school='enchantment',
                casting_time='1 action',
                spell_range='60ft',
                components=['verbal'],
                duration='1 round',
                description='You speak a one-word command to a creature you can see within range.')
