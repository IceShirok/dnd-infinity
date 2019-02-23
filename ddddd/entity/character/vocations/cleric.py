import ddddd.entity.character.spells
from ddddd.entity.character.base import AbilityScore, Skills
from ddddd.entity.character.spells import SpellTypes
from ddddd.entity.character import spells, feature, base
from ddddd.entity.character.vocation import Vocation


class Cleric(Vocation):
    def __init__(self, skill_proficiencies, languages, cantrips, cleric_domain):
        super(Cleric, self).__init__(name='Cleric',
                                     level=1,
                                     hit_die=8,
                                     proficiencies={
                                         base.ARMOR_PROFICIENCY: feature.ArmorProficiency(name='Armor Proficiency',
                                                                                          proficiencies=['light',
                                                                                                       'medium',
                                                                                                       'shields']),
                                         base.WEAPON_PROFICIENCY: feature.WeaponProficiency(name='Weapon Proficiency',
                                                                                            proficiencies=['simple']),
                                     },
                                     saving_throws=[AbilityScore.WIS, AbilityScore.CHA],
                                     skill_proficiencies=skill_proficiencies,
                                     features=None,
                                     spellcasting=None,
                                     asi=None)

        # It looks like order really does matter when initializing
        # The class broken when this was set before the parent __init__ was set.
        self.specialization = ClericDomain.get_cleric_domains()[cleric_domain]
        self._add_level_1_features(languages=languages, cantrips=cantrips)

    def _add_specialization_features(self, level, **kwargs):
        super(Cleric, self)._add_specialization_features(level, **kwargs)
        get_features = getattr(self.specialization, 'add_level_{}_features'.format(level), None)
        if get_features:
            add_level_features = get_features(**kwargs)
            if 'domain_spells' in add_level_features:
                self.spellcasting.append_cleric_domain_spells(add_level_features['domain_spells'])

    def _add_level_1_features(self, **kwargs):
        cantrips = kwargs['cantrips']
        spellcasting = ClericSpellcastingAbility(level=1,
                                                 cantrips=cantrips,
                                                 domain_spells=None)
        self.spellcasting = spellcasting

        super(Cleric, self)._add_level_1_features(**kwargs)
        languages = kwargs['languages']
        def_features = {
            'divine_domain': feature.Feature(name='Divine Domain',
                                             description='You have chosen to worship Ioun, goddess of knowledge. \
                                         Your divine domain is the Knowledge Domain.'),
            'blessings_of_knowledge': feature.Expertise(name='Blessings of Knowledge',
                                                        description='You become proficient in your choice of two of the following skills: \
                                                      Arcana, History, Nature, or Religion. Your proficiency bonus is doubled \
                                                      for any ability check you make that uses either of those skills.',
                                                        skills=[Skills.ARCANA, Skills.HISTORY],
                                                        proficiencies=None),
            'blessings_of_knowledge_languages': feature.LanguagesKnown(name='Blessings of Knowledge: Languages',
                                                                       description='At 1st level, you learn two languages of your choice.',
                                                                       languages=languages.languages),
        }
        for f_k, f in def_features.items():
            self._append_feature(f_k, f)

    def _add_level_2_features(self, **kwargs):
        super(Cleric, self)._add_level_2_features(**kwargs)
        self._append_feature('channel_divinity',
                             feature=feature.Feature(name='Channel Divinity',
                                                     description='At 2nd level, you gain the ability to channel divine energy directly \
                                                     from your deity, using that energy to fuel magical effects. When you finish a short \
                                                     or long rest, you regain your expended uses.'))

        self._append_feature('channel_divinity_turn_undead',
                             feature=feature.Feature(name='Channel Divinity: Turn Undead',
                                                     description='As an action, you present your holy symbol \
                                                 and speak a prayer censuring the undead.'))

        spellcasting = ClericSpellcastingAbility(level=2,
                                                 cantrips=self.spellcasting.cantrips,
                                                 domain_spells=self.spellcasting.casting_spells)
        self.spellcasting = spellcasting

    def _add_level_3_features(self, **kwargs):
        super(Cleric, self)._add_level_3_features(**kwargs)

        spellcasting = ClericSpellcastingAbility(level=3,
                                                 cantrips=self.spellcasting.cantrips,
                                                 domain_spells=self.spellcasting.casting_spells)
        self.spellcasting = spellcasting

    def _add_level_4_features(self, **kwargs):
        super(Cleric, self)._add_level_4_features(**kwargs)
        self._aggregate_asi_or_feat(kwargs, 4)

        new_cantrip = kwargs['cantrip_4']
        self.spellcasting.cantrips.append(new_cantrip)

        spellcasting = ClericSpellcastingAbility(level=4,
                                                 cantrips=self.spellcasting.cantrips,
                                                 domain_spells=self.spellcasting.casting_spells)
        self.spellcasting = spellcasting

    def _add_level_5_features(self, **kwargs):
        super(Cleric, self)._add_level_5_features(**kwargs)
        self._append_feature('channel_divinity_destroy_undead',
                             feature=feature.Feature(
                                 name='Channel Divinity: Destroy Undead (CR 1/2)',
                                 description='Starting at 5th level, when an undead fails its saving throw \
                                             against your Turn Undead feature, the creature is instantly destroyed \
                                             if its challenge rating is at or below CR 1/2.'))

        self._append_feature('channel_divinity',
                             feature=feature.Feature(name='Channel Divinity (2/rest)',
                                                     description='At 2nd level, you gain the ability to channel divine energy directly \
                                                 from your deity, using that energy to fuel magical effects. When you finish a short \
                                                 or long rest, you regain your expended uses.'))

        spellcasting = ClericSpellcastingAbility(level=5,
                                                 cantrips=self.spellcasting.cantrips,
                                                 domain_spells=self.spellcasting.casting_spells)
        self.spellcasting = spellcasting

    def _add_level_6_features(self, **kwargs):
        super(Cleric, self)._add_level_6_features(**kwargs)

        spellcasting = ClericSpellcastingAbility(level=6,
                                                 cantrips=self.spellcasting.cantrips,
                                                 domain_spells=self.spellcasting.casting_spells)
        self.spellcasting = spellcasting

    def _add_level_7_features(self, **kwargs):
        super(Cleric, self)._add_level_7_features(**kwargs)

        spellcasting = ClericSpellcastingAbility(level=7,
                                                 cantrips=self.spellcasting.cantrips,
                                                 domain_spells=self.spellcasting.casting_spells)
        self.spellcasting = spellcasting

    def _add_level_8_features(self, **kwargs):
        super(Cleric, self)._add_level_8_features(**kwargs)
        self._aggregate_asi_or_feat(kwargs, 8)

        self._append_feature('channel_divinity_destroy_undead',
                             feature=feature.Feature(
                                 name='Channel Divinity: Destroy Undead (CR 1)',
                                 description='Starting at 5th level, when an undead fails its saving throw \
                                            against your Turn Undead feature, the creature is instantly destroyed \
                                            if its challenge rating is at or below CR 1.'))

        spellcasting = ClericSpellcastingAbility(level=8,
                                                 cantrips=self.spellcasting.cantrips,
                                                 domain_spells=self.spellcasting.casting_spells)
        self.spellcasting = spellcasting

    def _add_level_9_features(self, **kwargs):
        super(Cleric, self)._add_level_9_features(**kwargs)

        spellcasting = ClericSpellcastingAbility(level=9,
                                                 cantrips=self.spellcasting.cantrips,
                                                 domain_spells=self.spellcasting.casting_spells)
        self.spellcasting = spellcasting

    def _add_level_10_features(self, **kwargs):
        super(Cleric, self)._add_level_10_features(**kwargs)
        self._append_feature('divine_intervention',
                             feature=feature.Feature(name='Divine Intervention',
                                                     description='Beginning at 10th level, you can call on your deity \
                                                 to intervene on your behalf when your need is great.'))

        new_cantrip = kwargs['cantrip_10']
        self.spellcasting.cantrips.append(new_cantrip)

        spellcasting = ClericSpellcastingAbility(level=10,
                                                 cantrips=self.spellcasting.cantrips,
                                                 domain_spells=self.spellcasting.casting_spells)
        self.spellcasting = spellcasting

    def _add_level_11_features(self, **kwargs):
        super(Cleric, self)._add_level_11_features(**kwargs)
        self._append_feature('channel_divinity_destroy_undead',
                             feature=feature.Feature(
                                 name='Channel Divinity: Destroy Undead (CR 2)',
                                 description='Starting at 5th level, when an undead fails its saving throw \
                                 against your Turn Undead feature, the creature is instantly destroyed \
                                 if its challenge rating is at or below CR 2.'))

        spellcasting = ClericSpellcastingAbility(level=11,
                                                 cantrips=self.spellcasting.cantrips,
                                                 domain_spells=self.spellcasting.casting_spells)
        self.spellcasting = spellcasting

    def _add_level_12_features(self, **kwargs):
        super(Cleric, self)._add_level_12_features(**kwargs)
        self._aggregate_asi_or_feat(kwargs, 12)

        spellcasting = ClericSpellcastingAbility(level=12,
                                                 cantrips=self.spellcasting.cantrips,
                                                 domain_spells=self.spellcasting.casting_spells)
        self.spellcasting = spellcasting

    def _add_level_13_features(self, **kwargs):
        super(Cleric, self)._add_level_13_features(**kwargs)

        spellcasting = ClericSpellcastingAbility(level=13,
                                                 cantrips=self.spellcasting.cantrips,
                                                 domain_spells=self.spellcasting.casting_spells)
        self.spellcasting = spellcasting

    def _add_level_14_features(self, **kwargs):
        super(Cleric, self)._add_level_14_features(**kwargs)
        self._append_feature('channel_divinity_destroy_undead',
                             feature=feature.Feature(
                                 name='Channel Divinity: Destroy Undead (CR 3)',
                                 description='Starting at 5th level, when an undead fails its saving throw \
                                 against your Turn Undead feature, the creature is instantly destroyed \
                                 if its challenge rating is at or below CR 3.'))

        spellcasting = ClericSpellcastingAbility(level=14,
                                                 cantrips=self.spellcasting.cantrips,
                                                 domain_spells=self.spellcasting.casting_spells)
        self.spellcasting = spellcasting

    def _add_level_15_features(self, **kwargs):
        super(Cleric, self)._add_level_15_features(**kwargs)

        spellcasting = ClericSpellcastingAbility(level=15,
                                                 cantrips=self.spellcasting.cantrips,
                                                 domain_spells=self.spellcasting.casting_spells)
        self.spellcasting = spellcasting

    def _add_level_16_features(self, **kwargs):
        super(Cleric, self)._add_level_16_features(**kwargs)
        self._aggregate_asi_or_feat(kwargs, 16)

        spellcasting = ClericSpellcastingAbility(level=16,
                                                 cantrips=self.spellcasting.cantrips,
                                                 domain_spells=self.spellcasting.casting_spells)
        self.spellcasting = spellcasting

    def _add_level_17_features(self, **kwargs):
        super(Cleric, self)._add_level_17_features(**kwargs)
        self._append_feature('channel_divinity_destroy_undead',
                             feature=feature.Feature(
                                 name='Channel Divinity: Destroy Undead (CR 4)',
                                 description='Starting at 5th level, when an undead fails its saving throw \
                                 against your Turn Undead feature, the creature is instantly destroyed \
                                 if its challenge rating is at or below CR 4.'))

        spellcasting = ClericSpellcastingAbility(level=17,
                                                 cantrips=self.spellcasting.cantrips,
                                                 domain_spells=self.spellcasting.casting_spells)
        self.spellcasting = spellcasting

    def _add_level_18_features(self, **kwargs):
        super(Cleric, self)._add_level_18_features(**kwargs)
        self._append_feature('channel_divinity',
                             feature=feature.Feature(name='Channel Divinity (3/rest)',
                                                     description='At 2nd level, you gain the ability to channel divine energy directly \
                                                 from your deity, using that energy to fuel magical effects. When you finish a short \
                                                 or long rest, you regain your expended uses.'))

        spellcasting = ClericSpellcastingAbility(level=18,
                                                 cantrips=self.spellcasting.cantrips,
                                                 domain_spells=self.spellcasting.casting_spells)
        self.spellcasting = spellcasting

    def _add_level_19_features(self, **kwargs):
        super(Cleric, self)._add_level_19_features(**kwargs)
        self._aggregate_asi_or_feat(kwargs, 19)

        spellcasting = ClericSpellcastingAbility(level=19,
                                                 cantrips=self.spellcasting.cantrips,
                                                 domain_spells=self.spellcasting.casting_spells)
        self.spellcasting = spellcasting

    def _add_level_20_features(self, **kwargs):
        super(Cleric, self)._add_level_20_features(**kwargs)
        self._append_feature('divine_intervention',
                             feature=feature.Feature(name='Improved Divine Intervention',
                                                     description='At 20th level, your call for intervention succeeds automatically, \
                                                 no roll required.'))

        spellcasting = ClericSpellcastingAbility(level=20,
                                                 cantrips=self.spellcasting.cantrips,
                                                 domain_spells=self.spellcasting.casting_spells)
        self.spellcasting = spellcasting


class PotentSpellcasting(feature.EnhanceDamage):
    def __init__(self, wis_mod):
        super(PotentSpellcasting, self).__init__(name='Potent Spellcasting',
                                                 description='Starting at 8th level, you add your Wisdom modifier \
                                                 to the damage you deal with any cleric cantrip.',
                                                 attack_bonus=wis_mod)

    def qualifies(self, spell):
        return isinstance(spell, spells.DamageCantrip)


class ClericSpellcastingAbility(spells.SpellcastingAbility):
    """
    Clerics prepare spells from a pre-determined list of cleric spells. The number of spells
    a cleric can prepare is determined by some varying factors.
    In addition, clerics get domain-specific spells that are considered part of their spell list
    and are already "prepared".
    """
    def __init__(self, level, cantrips, domain_spells=None):
        self.level = level
        spell_slots = spells.get_spell_slot_by_level(level)
        super(ClericSpellcastingAbility, self).__init__(spellcasting_ability=base.AbilityScore.WIS,
                                                        spell_slots=spell_slots,
                                                        casting_spells=domain_spells,
                                                        num_cantrips_known=spells.cantrips_by_level(level),
                                                        cantrips=cantrips)

    def append_cleric_domain_spells(self, spells):
        self.casting_spells.extend(spells)

    def num_spells_known(self, ability_scores):
        """
        The number of spells that a cleric can prepare is the cleric level + the cleric's wisdom modifier.
        :param ability_scores: the PC's ability scores
        :return: the total number of spells that the cleric can prepare
        """
        return self.level + ability_scores[self.spellcasting_ability].modifier

    def _verify(self):
        # TODO this part is tricky because it requires knowing the PC's WIS modifier to determine the number of spells.
        return {}
        # super(ClericSpellcastingAbility, self)._verify()
        # spells_ = list(filter(lambda x: x.level != base.SpellTypes.CANTRIPS, self.list_spells_known))
        # if len(spells_) != self.num_spells_known:
        #     raise ValueError('Must have {} spells but inputted {} spells!'.format(self.num_spells_known, len(spells_)))


##############################
# CLERIC DOMAINS
##############################

class ClericDomain(object):
    """
    The cleric subclass.
    """

    @staticmethod
    def get_cleric_domains():
        return {
            'knowledge': KnowledgeDomain(),
        }

    @staticmethod
    def get_cleric_domain(name):
        return ClericDomain.get_cleric_domains()[name]

    def add_level_1_features(self, **kwargs):
        raise NotImplementedError()

    def add_level_2_features(self, **kwargs):
        raise NotImplementedError()

    def add_level_3_features(self, **kwargs):
        raise NotImplementedError()

    def add_level_5_features(self, **kwargs):
        raise NotImplementedError()

    def add_level_6_features(self, **kwargs):
        raise NotImplementedError()

    def add_level_7_features(self, **kwargs):
        raise NotImplementedError()

    def add_level_8_features(self, **kwargs):
        raise NotImplementedError()

    def add_level_9_features(self, **kwargs):
        raise NotImplementedError()

    def add_level_17_features(self, **kwargs):
        raise NotImplementedError()


class KnowledgeDomain(ClericDomain):

    def add_level_1_features(self, **kwargs):
        new_features = {}

        simple_spell_list = [
            ('Command', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Identify', ddddd.entity.character.spells.SpellTypes.FIRST),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)

        new_stuff = {
            'features': new_features,
            'domain_spells': casting_spells,
        }

        return new_stuff

    def add_level_2_features(self, **kwargs):
        new_features = {
            'channel_divinity_knowledge_of_the_ages': feature.Feature(name='Channel Divinity: Knowledge of the Ages',
                                                                      description='Starting at 2nd level, you can use \
                                                 your Channel Divinity to tap into a divine well of knowledge. \
                                                 As an action, you choose one skill or tool. \
                                                 For 10 minutes, you have proficiency with the chosen skill or tool.')
        }
        new_stuff = {'features': new_features}
        return new_stuff

    def add_level_3_features(self, **kwargs):
        new_features = {}

        simple_spell_list = [
            ('Augury', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Suggestion', ddddd.entity.character.spells.SpellTypes.SECOND),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)

        new_stuff = {
            'features': new_features,
            'domain_spells': casting_spells,
        }

        return new_stuff

    def add_level_5_features(self, **kwargs):
        new_features = {}

        simple_spell_list = [
            ('Speak with Dead', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Tongues', ddddd.entity.character.spells.SpellTypes.THIRD),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)

        new_stuff = {
            'features': new_features,
            'domain_spells': casting_spells,
        }

        return new_stuff

    def add_level_6_features(self, **kwargs):
        new_features = {
            'channel_divinity_read_thoughts': feature.Feature(name='Channel Divinity: Read Thoughts',
                                                              description='At 6th level, you can use your \
                                                              Channel Divinity to read a creature''s thoguhts.')
        }
        new_stuff = {'features': new_features}
        return new_stuff

    def add_level_7_features(self, **kwargs):
        new_features = {}

        simple_spell_list = [
            ('Arcane Eye', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Confusion', ddddd.entity.character.spells.SpellTypes.FOURTH),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)

        new_stuff = {
            'features': new_features,
            'domain_spells': casting_spells,
        }

        return new_stuff

    def add_level_8_features(self, **kwargs):
        # TODO fix the wisdom modifier
        new_features = {
            'potent_spellcasting': PotentSpellcasting(wis_mod=4)
        }
        new_stuff = {'features': new_features}
        return new_stuff

    def add_level_9_features(self, **kwargs):
        new_features = {}

        simple_spell_list = [
            ('Legend Lore', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Scrying', ddddd.entity.character.spells.SpellTypes.FIFTH),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)

        new_stuff = {
            'features': new_features,
            'domain_spells': casting_spells,
        }

        return new_stuff

    def add_level_17_features(self, **kwargs):
        new_features = {
            'visions_of_the_past': feature.Feature(name='Visions of the Past',
                                                   description='Starting at 17th level, you can call up \
                                                   visions of the past that relate to an object you hold or your immediate surroundings.')
        }
        new_stuff = {'features': new_features}
        return new_stuff
