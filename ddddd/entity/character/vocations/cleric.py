import ddddd.entity.character.spells
from ddddd.entity.character.base import AbilityScore, Skills
from ddddd.entity.character.spells import SpellTypes
from ddddd.entity.character import spells, feature, base
from ddddd.entity.character.vocation import Vocation


class Cleric(Vocation):
    FAVORED_ENEMY = 'favored_enemy'
    ENEMIES = 'enemies'
    NATURAL_EXPLORER = 'natural_explorer'
    TERRAINS = 'terrains'
    FIGHTING_STYLE = 'fighting_style'
    STYLES = 'styles'

    def __init__(self, skill_proficiencies, languages, cantrips):
        self.specialization = KnowledgeDomainStrategy()
        # self._add_specialization_features(self.level, **kwargs)
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

        simple_spell_list = [
            ('Command', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Identify', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Cure Wounds', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Bless', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Healing Word', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Sanctuary', ddddd.entity.character.spells.SpellTypes.FIRST),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)
        spellcasting = ClericSpellcastingAbility(list_spells_known=casting_spells,
                                                 spell_slots=spells.get_spell_slot_by_level(1),
                                                 num_spells_known=3 + 1 + 2,
                                                 num_cantrips_known=spells.cantrips_by_level(3), cantrips=cantrips)

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
                                     features=def_features,
                                     spellcasting=spellcasting,
                                     asi=None)

    def _add_level_2_features(self, **kwargs):
        self._add_specialization_features(self.level, **kwargs)
        self._append_feature('channel_divinity',
                             feature=feature.Feature(name='Channel Divinity',
                                                     description='At 2nd level, you gain the ability to channel divine energy directly \
                                                 from your deity, using that energy to fuel magical effects. When you finish a short \
                                                 or long rest, you regain your expended uses.'))

        self._append_feature('channel_divinity_turn_undead',
                             feature=feature.Feature(name='Channel Divinity: Turn Undead',
                                                     description='As an action, you present your holy symbol \
                                                 and speak a prayer censuring the undead.'))

        self._append_feature('channel_divinity_knowledge_of_the_ages',
                             feature=feature.Feature(name='Channel Divinity: Knowledge of the Ages',
                                                     description='Starting at 2nd level, you can use your Channel Divinity to tap into \
                                                 a divine well of knowledge. As an action, you choose one skill or tool. \
                                                 For 10 minutes, you have proficiency with the chosen skill or tool.'))

        simple_spell_list = [
            ('Command', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Identify', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Cure Wounds', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Bless', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Healing Word', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Inflict Wounds', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Sanctuary', ddddd.entity.character.spells.SpellTypes.FIRST),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)
        spellcasting = ClericSpellcastingAbility(list_spells_known=casting_spells,
                                                 spell_slots=spells.get_spell_slot_by_level(2),
                                                 num_spells_known=3 + 2 + 2,
                                                 num_cantrips_known=spells.cantrips_by_level(3), cantrips=self.spellcasting.cantrips)
        self.spellcasting = spellcasting

    def _add_level_3_features(self, **kwargs):
        self._add_specialization_features(self.level, **kwargs)
        simple_spell_list = [
            ('Command', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Identify', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Cure Wounds', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Bless', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Healing Word', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Sanctuary', ddddd.entity.character.spells.SpellTypes.FIRST),

            ('Enhance Ability', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Lesser Restoration', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Augury', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Suggestion', ddddd.entity.character.spells.SpellTypes.SECOND),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)
        spellcasting = ClericSpellcastingAbility(list_spells_known=casting_spells,
                                                 spell_slots=spells.get_spell_slot_by_level(3),
                                                 num_spells_known=3 + 3 + 4,
                                                 num_cantrips_known=spells.cantrips_by_level(3), cantrips=self.spellcasting.cantrips)
        self.spellcasting = spellcasting

    def _add_level_4_features(self, **kwargs):
        self._aggregate_asi_or_feat(kwargs, 4)

        new_cantrip = kwargs['cantrip_4']
        self.spellcasting.cantrips.append(new_cantrip)
        simple_spell_list = [
            ('Command', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Identify', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Cure Wounds', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Bless', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Healing Word', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Sanctuary', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Guiding Bolt', ddddd.entity.character.spells.SpellTypes.FIRST),

            ('Enhance Ability', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Lesser Restoration', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Augury', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Suggestion', ddddd.entity.character.spells.SpellTypes.SECOND),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)
        spellcasting = ClericSpellcastingAbility(list_spells_known=casting_spells,
                                                 spell_slots=spells.get_spell_slot_by_level(4),
                                                 num_spells_known=4 + 4 + 4,
                                                 num_cantrips_known=spells.cantrips_by_level(4), cantrips=self.spellcasting.cantrips)
        self.spellcasting = spellcasting

    def _add_level_5_features(self, **kwargs):
        self._append_feature('channel_divinity_destroy_undead',
                             feature=feature.Feature(
                                 name='Channel Divinity: Destroy Undead (CR 1/2)',
                                 description='Starting at 5th level, when an undead fails its saving throw \
                                             against your Turn Undead feature, the creature is instantly destroyed \
                                             if its challenge rating is at or below CR 1/2.'))

        self._add_specialization_features(self.level, **kwargs)
        # TODO work on the mechanic to override stuff
        self._append_feature('channel_divinity',
                             feature=feature.Feature(name='Channel Divinity (2/rest)',
                                                     description='At 2nd level, you gain the ability to channel divine energy directly \
                                                 from your deity, using that energy to fuel magical effects. When you finish a short \
                                                 or long rest, you regain your expended uses.'))

        simple_spell_list = [
            ('Command', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Identify', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Cure Wounds', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Bless', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Healing Word', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Sanctuary', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Guiding Bolt', ddddd.entity.character.spells.SpellTypes.FIRST),

            ('Enhance Ability', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Lesser Restoration', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Spiritual Weapon', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Augury', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Suggestion', ddddd.entity.character.spells.SpellTypes.SECOND),

            ('Nondetection', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Speak with Dead', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Tongues', ddddd.entity.character.spells.SpellTypes.THIRD),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)
        spellcasting = ClericSpellcastingAbility(list_spells_known=casting_spells,
                                                 spell_slots=spells.get_spell_slot_by_level(5),
                                                 num_spells_known=4 + 5 + 6,
                                                 num_cantrips_known=spells.cantrips_by_level(4), cantrips=self.spellcasting.cantrips)
        self.spellcasting = spellcasting

    def _add_level_6_features(self, **kwargs):
        self._append_feature('channel_divinity_read_thoughts',
                             feature=feature.Feature(name='Channel Divinity: Read Thoughts',
                                                     description='At 6th level, you can use your Channel Divinity to read \
                                                 a creature''s thoguhts.'))
        self._add_specialization_features(self.level, **kwargs)

        simple_spell_list = [
            ('Command', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Identify', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Cure Wounds', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Bless', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Healing Word', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Sanctuary', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Guiding Bolt', ddddd.entity.character.spells.SpellTypes.FIRST),

            ('Enhance Ability', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Lesser Restoration', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Spiritual Weapon', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Augury', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Suggestion', ddddd.entity.character.spells.SpellTypes.SECOND),

            ('Nondetection', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Speak with Dead', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Tongues', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Bestow Curse', ddddd.entity.character.spells.SpellTypes.THIRD),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)
        spellcasting = ClericSpellcastingAbility(list_spells_known=casting_spells,
                                                 spell_slots=spells.get_spell_slot_by_level(6),
                                                 num_spells_known=4 + 6 + 6,
                                                 num_cantrips_known=spells.cantrips_by_level(4), cantrips=self.spellcasting.cantrips)
        self.spellcasting = spellcasting

    def _add_level_7_features(self, **kwargs):
        # TODO fix the wisdom modifier
        self._append_feature('potent_spellcasting',
                             feature=PotentSpellcasting(wis_mod=4))
        self._add_specialization_features(self.level, **kwargs)

        simple_spell_list = [
            ('Command', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Identify', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Cure Wounds', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Bless', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Healing Word', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Sanctuary', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Guiding Bolt', ddddd.entity.character.spells.SpellTypes.FIRST),

            ('Enhance Ability', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Lesser Restoration', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Spiritual Weapon', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Augury', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Suggestion', ddddd.entity.character.spells.SpellTypes.SECOND),

            ('Nondetection', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Speak with Dead', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Tongues', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Bestow Curse', ddddd.entity.character.spells.SpellTypes.THIRD),

            ('Banishment', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Arcane Eye', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Confusion', ddddd.entity.character.spells.SpellTypes.FOURTH),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)
        spellcasting = ClericSpellcastingAbility(list_spells_known=casting_spells,
                                                 spell_slots=spells.get_spell_slot_by_level(7),
                                                 num_spells_known=4 + 7 + 8,
                                                 num_cantrips_known=spells.cantrips_by_level(4), cantrips=self.spellcasting.cantrips)
        self.spellcasting = spellcasting

    def _add_level_8_features(self, **kwargs):
        self._aggregate_asi_or_feat(kwargs, 8)
        self._add_specialization_features(self.level, **kwargs)

        self._append_feature('channel_divinity_destroy_undead',
                             feature=feature.Feature(
                                 name='Channel Divinity: Destroy Undead (CR 1)',
                                 description='Starting at 5th level, when an undead fails its saving throw \
                                            against your Turn Undead feature, the creature is instantly destroyed \
                                            if its challenge rating is at or below CR 1.'))

        simple_spell_list = [
            ('Command', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Identify', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Cure Wounds', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Bless', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Healing Word', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Sanctuary', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Guiding Bolt', ddddd.entity.character.spells.SpellTypes.FIRST),

            ('Enhance Ability', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Lesser Restoration', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Spiritual Weapon', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Augury', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Suggestion', ddddd.entity.character.spells.SpellTypes.SECOND),

            ('Nondetection', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Speak with Dead', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Tongues', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Bestow Curse', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Spirit Guardians', ddddd.entity.character.spells.SpellTypes.THIRD),

            ('Banishment', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Arcane Eye', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Confusion', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Freedom of Movement', ddddd.entity.character.spells.SpellTypes.FOURTH),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)
        spellcasting = ClericSpellcastingAbility(list_spells_known=casting_spells,
                                                 spell_slots=spells.get_spell_slot_by_level(8),
                                                 num_spells_known=5 + 8 + 8,
                                                 num_cantrips_known=spells.cantrips_by_level(4), cantrips=self.spellcasting.cantrips)
        self.spellcasting = spellcasting

    def _add_level_9_features(self, **kwargs):
        self._add_specialization_features(self.level, **kwargs)
        simple_spell_list = [
            ('Command', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Identify', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Cure Wounds', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Bless', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Healing Word', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Sanctuary', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Guiding Bolt', ddddd.entity.character.spells.SpellTypes.FIRST),

            ('Enhance Ability', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Lesser Restoration', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Spiritual Weapon', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Augury', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Suggestion', ddddd.entity.character.spells.SpellTypes.SECOND),

            ('Nondetection', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Speak with Dead', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Tongues', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Bestow Curse', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Spirit Guardians', ddddd.entity.character.spells.SpellTypes.THIRD),

            ('Banishment', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Arcane Eye', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Confusion', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Freedom of Movement', ddddd.entity.character.spells.SpellTypes.FOURTH),

            ('Geas', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Legend Lore', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Scrying', ddddd.entity.character.spells.SpellTypes.FIFTH),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)
        spellcasting = ClericSpellcastingAbility(list_spells_known=casting_spells,
                                                 spell_slots=spells.get_spell_slot_by_level(9),
                                                 num_spells_known=5 + 9 + 10,
                                                 num_cantrips_known=spells.cantrips_by_level(4), cantrips=self.spellcasting.cantrips)
        self.spellcasting = spellcasting

    def _add_level_10_features(self, **kwargs):
        self._append_feature('divine_intervention',
                             feature=feature.Feature(name='Divine Intervention',
                                                     description='Beginning at 10th level, you can call on your deity \
                                                 to intervene on your behalf when your need is great.'))

        new_cantrip = kwargs['cantrip_10']
        self.spellcasting.cantrips.append(new_cantrip)

        simple_spell_list = [
            ('Command', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Identify', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Cure Wounds', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Bless', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Healing Word', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Sanctuary', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Guiding Bolt', ddddd.entity.character.spells.SpellTypes.FIRST),

            ('Enhance Ability', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Lesser Restoration', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Spiritual Weapon', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Augury', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Suggestion', ddddd.entity.character.spells.SpellTypes.SECOND),

            ('Nondetection', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Speak with Dead', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Tongues', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Bestow Curse', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Spirit Guardians', ddddd.entity.character.spells.SpellTypes.THIRD),

            ('Banishment', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Arcane Eye', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Confusion', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Freedom of Movement', ddddd.entity.character.spells.SpellTypes.FOURTH),

            ('Geas', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Legend Lore', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Scrying', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Flame Strike', ddddd.entity.character.spells.SpellTypes.FIFTH),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)
        spellcasting = ClericSpellcastingAbility(list_spells_known=casting_spells,
                                                 spell_slots=spells.get_spell_slot_by_level(10),
                                                 num_spells_known=5 + 10 + 10,
                                                 num_cantrips_known=spells.cantrips_by_level(5), cantrips=self.spellcasting.cantrips)
        self.spellcasting = spellcasting

    def _add_level_11_features(self, **kwargs):
        self._append_feature('channel_divinity_destroy_undead',
                             feature=feature.Feature(
                                 name='Channel Divinity: Destroy Undead (CR 2)',
                                 description='Starting at 5th level, when an undead fails its saving throw \
                                 against your Turn Undead feature, the creature is instantly destroyed \
                                 if its challenge rating is at or below CR 2.'))

        simple_spell_list = [
            ('Command', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Identify', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Cure Wounds', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Bless', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Healing Word', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Sanctuary', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Guiding Bolt', ddddd.entity.character.spells.SpellTypes.FIRST),

            ('Enhance Ability', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Lesser Restoration', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Spiritual Weapon', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Augury', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Suggestion', ddddd.entity.character.spells.SpellTypes.SECOND),

            ('Nondetection', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Speak with Dead', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Tongues', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Bestow Curse', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Spirit Guardians', ddddd.entity.character.spells.SpellTypes.THIRD),

            ('Banishment', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Arcane Eye', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Confusion', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Freedom of Movement', ddddd.entity.character.spells.SpellTypes.FOURTH),

            ('Geas', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Legend Lore', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Scrying', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Flame Strike', ddddd.entity.character.spells.SpellTypes.FIFTH),

            ('Find the Path', ddddd.entity.character.spells.SpellTypes.SIXTH),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)
        spellcasting = ClericSpellcastingAbility(list_spells_known=casting_spells,
                                                 spell_slots=spells.get_spell_slot_by_level(11),
                                                 num_spells_known=5 + 11 + 10,
                                                 num_cantrips_known=spells.cantrips_by_level(5), cantrips=self.spellcasting.cantrips)
        self.spellcasting = spellcasting

    def _add_level_12_features(self, **kwargs):
        self._aggregate_asi_or_feat(kwargs, 12)

        simple_spell_list = [
            ('Command', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Identify', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Cure Wounds', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Bless', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Healing Word', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Sanctuary', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Guiding Bolt', ddddd.entity.character.spells.SpellTypes.FIRST),

            ('Enhance Ability', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Lesser Restoration', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Spiritual Weapon', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Augury', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Suggestion', ddddd.entity.character.spells.SpellTypes.SECOND),

            ('Nondetection', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Speak with Dead', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Tongues', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Bestow Curse', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Spirit Guardians', ddddd.entity.character.spells.SpellTypes.THIRD),

            ('Banishment', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Arcane Eye', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Confusion', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Freedom of Movement', ddddd.entity.character.spells.SpellTypes.FOURTH),

            ('Geas', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Legend Lore', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Scrying', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Flame Strike', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Greater Restoration', ddddd.entity.character.spells.SpellTypes.FIFTH),

            ('Find the Path', ddddd.entity.character.spells.SpellTypes.SIXTH),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)
        spellcasting = ClericSpellcastingAbility(list_spells_known=casting_spells,
                                                 spell_slots=spells.get_spell_slot_by_level(12),
                                                 num_spells_known=5 + 12 + 10,
                                                 num_cantrips_known=spells.cantrips_by_level(5), cantrips=self.spellcasting.cantrips)
        self.spellcasting = spellcasting

    def _add_level_13_features(self, **kwargs):
        simple_spell_list = [
            ('Command', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Identify', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Cure Wounds', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Bless', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Healing Word', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Sanctuary', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Guiding Bolt', ddddd.entity.character.spells.SpellTypes.FIRST),

            ('Enhance Ability', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Lesser Restoration', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Spiritual Weapon', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Augury', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Suggestion', ddddd.entity.character.spells.SpellTypes.SECOND),

            ('Nondetection', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Speak with Dead', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Tongues', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Bestow Curse', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Spirit Guardians', ddddd.entity.character.spells.SpellTypes.THIRD),

            ('Banishment', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Arcane Eye', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Confusion', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Freedom of Movement', ddddd.entity.character.spells.SpellTypes.FOURTH),

            ('Geas', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Legend Lore', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Scrying', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Flame Strike', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Greater Restoration', ddddd.entity.character.spells.SpellTypes.FIFTH),

            ('Find the Path', ddddd.entity.character.spells.SpellTypes.SIXTH),

            ('Plane Shift', ddddd.entity.character.spells.SpellTypes.SEVENTH),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)
        spellcasting = ClericSpellcastingAbility(list_spells_known=casting_spells,
                                                 spell_slots=spells.get_spell_slot_by_level(13),
                                                 num_spells_known=5 + 13 + 10,
                                                 num_cantrips_known=spells.cantrips_by_level(5), cantrips=self.spellcasting.cantrips)
        self.spellcasting = spellcasting

    def _add_level_14_features(self, **kwargs):
        self._append_feature('channel_divinity_destroy_undead',
                             feature=feature.Feature(
                                 name='Channel Divinity: Destroy Undead (CR 3)',
                                 description='Starting at 5th level, when an undead fails its saving throw \
                                 against your Turn Undead feature, the creature is instantly destroyed \
                                 if its challenge rating is at or below CR 3.'))

        simple_spell_list = [
            ('Command', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Identify', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Cure Wounds', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Bless', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Healing Word', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Sanctuary', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Guiding Bolt', ddddd.entity.character.spells.SpellTypes.FIRST),

            ('Enhance Ability', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Lesser Restoration', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Spiritual Weapon', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Augury', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Suggestion', ddddd.entity.character.spells.SpellTypes.SECOND),

            ('Nondetection', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Speak with Dead', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Tongues', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Bestow Curse', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Spirit Guardians', ddddd.entity.character.spells.SpellTypes.THIRD),

            ('Banishment', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Arcane Eye', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Confusion', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Freedom of Movement', ddddd.entity.character.spells.SpellTypes.FOURTH),

            ('Geas', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Legend Lore', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Scrying', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Flame Strike', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Greater Restoration', ddddd.entity.character.spells.SpellTypes.FIFTH),

            ('Find the Path', ddddd.entity.character.spells.SpellTypes.SIXTH),
            ('Heal', ddddd.entity.character.spells.SpellTypes.SIXTH),

            ('Plane Shift', ddddd.entity.character.spells.SpellTypes.SEVENTH),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)
        spellcasting = ClericSpellcastingAbility(list_spells_known=casting_spells,
                                                 spell_slots=spells.get_spell_slot_by_level(14),
                                                 num_spells_known=5 + 14 + 10,
                                                 num_cantrips_known=spells.cantrips_by_level(5), cantrips=self.spellcasting.cantrips)
        self.spellcasting = spellcasting

    def _add_level_15_features(self, **kwargs):
        simple_spell_list = [
            ('Command', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Identify', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Cure Wounds', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Bless', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Healing Word', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Sanctuary', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Guiding Bolt', ddddd.entity.character.spells.SpellTypes.FIRST),

            ('Enhance Ability', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Lesser Restoration', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Spiritual Weapon', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Augury', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Suggestion', ddddd.entity.character.spells.SpellTypes.SECOND),

            ('Nondetection', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Speak with Dead', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Tongues', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Bestow Curse', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Spirit Guardians', ddddd.entity.character.spells.SpellTypes.THIRD),

            ('Banishment', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Arcane Eye', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Confusion', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Freedom of Movement', ddddd.entity.character.spells.SpellTypes.FOURTH),

            ('Geas', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Legend Lore', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Scrying', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Flame Strike', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Greater Restoration', ddddd.entity.character.spells.SpellTypes.FIFTH),

            ('Find the Path', ddddd.entity.character.spells.SpellTypes.SIXTH),
            ('Heal', ddddd.entity.character.spells.SpellTypes.SIXTH),

            ('Plane Shift', ddddd.entity.character.spells.SpellTypes.SEVENTH),

            ('Earthquake', ddddd.entity.character.spells.SpellTypes.EIGHTH),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)
        spellcasting = ClericSpellcastingAbility(list_spells_known=casting_spells,
                                                 spell_slots=spells.get_spell_slot_by_level(15),
                                                 num_spells_known=5 + 15 + 10,
                                                 num_cantrips_known=spells.cantrips_by_level(5), cantrips=self.spellcasting.cantrips)
        self.spellcasting = spellcasting

    def _add_level_16_features(self, **kwargs):
        self._aggregate_asi_or_feat(kwargs, 16)

        simple_spell_list = [
            ('Command', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Identify', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Cure Wounds', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Bless', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Healing Word', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Sanctuary', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Guiding Bolt', ddddd.entity.character.spells.SpellTypes.FIRST),

            ('Enhance Ability', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Lesser Restoration', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Spiritual Weapon', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Augury', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Suggestion', ddddd.entity.character.spells.SpellTypes.SECOND),

            ('Nondetection', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Speak with Dead', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Tongues', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Bestow Curse', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Spirit Guardians', ddddd.entity.character.spells.SpellTypes.THIRD),

            ('Banishment', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Arcane Eye', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Confusion', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Freedom of Movement', ddddd.entity.character.spells.SpellTypes.FOURTH),

            ('Geas', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Legend Lore', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Scrying', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Flame Strike', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Greater Restoration', ddddd.entity.character.spells.SpellTypes.FIFTH),

            ('Find the Path', ddddd.entity.character.spells.SpellTypes.SIXTH),
            ('Heal', ddddd.entity.character.spells.SpellTypes.SIXTH),

            ('Plane Shift', ddddd.entity.character.spells.SpellTypes.SEVENTH),
            ('Fire Storm', ddddd.entity.character.spells.SpellTypes.SEVENTH),

            ('Earthquake', ddddd.entity.character.spells.SpellTypes.EIGHTH),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)
        spellcasting = ClericSpellcastingAbility(list_spells_known=casting_spells,
                                                 spell_slots=spells.get_spell_slot_by_level(16),
                                                 num_spells_known=5 + 16 + 10,
                                                 num_cantrips_known=spells.cantrips_by_level(5), cantrips=self.spellcasting.cantrips)
        self.spellcasting = spellcasting

    def _add_level_17_features(self, **kwargs):
        self._add_specialization_features(self.level, **kwargs)
        self._append_feature('channel_divinity_destroy_undead',
                             feature=feature.Feature(
                                 name='Channel Divinity: Destroy Undead (CR 4)',
                                 description='Starting at 5th level, when an undead fails its saving throw \
                                 against your Turn Undead feature, the creature is instantly destroyed \
                                 if its challenge rating is at or below CR 4.'))

        simple_spell_list = [
            ('Command', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Identify', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Cure Wounds', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Bless', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Healing Word', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Sanctuary', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Guiding Bolt', ddddd.entity.character.spells.SpellTypes.FIRST),

            ('Enhance Ability', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Lesser Restoration', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Spiritual Weapon', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Augury', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Suggestion', ddddd.entity.character.spells.SpellTypes.SECOND),

            ('Nondetection', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Speak with Dead', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Tongues', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Bestow Curse', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Spirit Guardians', ddddd.entity.character.spells.SpellTypes.THIRD),

            ('Banishment', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Arcane Eye', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Confusion', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Freedom of Movement', ddddd.entity.character.spells.SpellTypes.FOURTH),

            ('Geas', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Legend Lore', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Scrying', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Flame Strike', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Greater Restoration', ddddd.entity.character.spells.SpellTypes.FIFTH),

            ('Find the Path', ddddd.entity.character.spells.SpellTypes.SIXTH),
            ('Heal', ddddd.entity.character.spells.SpellTypes.SIXTH),

            ('Plane Shift', ddddd.entity.character.spells.SpellTypes.SEVENTH),
            ('Fire Storm', ddddd.entity.character.spells.SpellTypes.SEVENTH),

            ('Earthquake', ddddd.entity.character.spells.SpellTypes.EIGHTH),

            ('Gate', ddddd.entity.character.spells.SpellTypes.NINTH),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)
        spellcasting = ClericSpellcastingAbility(list_spells_known=casting_spells,
                                                 spell_slots=spells.get_spell_slot_by_level(17),
                                                 num_spells_known=5 + 17 + 10,
                                                 num_cantrips_known=spells.cantrips_by_level(5), cantrips=self.spellcasting.cantrips)
        self.spellcasting = spellcasting

    def _add_level_18_features(self, **kwargs):
        self._append_feature('channel_divinity',
                             feature=feature.Feature(name='Channel Divinity (3/rest)',
                                                     description='At 2nd level, you gain the ability to channel divine energy directly \
                                                 from your deity, using that energy to fuel magical effects. When you finish a short \
                                                 or long rest, you regain your expended uses.'))

        simple_spell_list = [
            ('Command', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Identify', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Cure Wounds', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Bless', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Healing Word', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Sanctuary', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Guiding Bolt', ddddd.entity.character.spells.SpellTypes.FIRST),

            ('Enhance Ability', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Lesser Restoration', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Spiritual Weapon', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Augury', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Suggestion', ddddd.entity.character.spells.SpellTypes.SECOND),

            ('Nondetection', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Speak with Dead', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Tongues', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Bestow Curse', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Spirit Guardians', ddddd.entity.character.spells.SpellTypes.THIRD),

            ('Banishment', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Arcane Eye', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Confusion', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Freedom of Movement', ddddd.entity.character.spells.SpellTypes.FOURTH),

            ('Geas', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Legend Lore', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Scrying', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Flame Strike', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Greater Restoration', ddddd.entity.character.spells.SpellTypes.FIFTH),

            ('Find the Path', ddddd.entity.character.spells.SpellTypes.SIXTH),
            ('Heal', ddddd.entity.character.spells.SpellTypes.SIXTH),
            ('Harm', ddddd.entity.character.spells.SpellTypes.SIXTH),

            ('Plane Shift', ddddd.entity.character.spells.SpellTypes.SEVENTH),
            ('Fire Storm', ddddd.entity.character.spells.SpellTypes.SEVENTH),

            ('Earthquake', ddddd.entity.character.spells.SpellTypes.EIGHTH),

            ('Gate', ddddd.entity.character.spells.SpellTypes.NINTH),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)
        spellcasting = ClericSpellcastingAbility(list_spells_known=casting_spells,
                                                 spell_slots=spells.get_spell_slot_by_level(18),
                                                 num_spells_known=5 + 18 + 10,
                                                 num_cantrips_known=spells.cantrips_by_level(5), cantrips=self.spellcasting.cantrips)
        self.spellcasting = spellcasting

    def _add_level_19_features(self, **kwargs):
        self._aggregate_asi_or_feat(kwargs, 19)

        simple_spell_list = [
            ('Command', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Identify', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Cure Wounds', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Bless', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Healing Word', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Sanctuary', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Guiding Bolt', ddddd.entity.character.spells.SpellTypes.FIRST),

            ('Enhance Ability', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Lesser Restoration', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Spiritual Weapon', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Augury', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Suggestion', ddddd.entity.character.spells.SpellTypes.SECOND),

            ('Nondetection', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Speak with Dead', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Tongues', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Bestow Curse', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Spirit Guardians', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Revivify', ddddd.entity.character.spells.SpellTypes.THIRD),

            ('Banishment', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Arcane Eye', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Confusion', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Freedom of Movement', ddddd.entity.character.spells.SpellTypes.FOURTH),

            ('Geas', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Legend Lore', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Scrying', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Flame Strike', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Greater Restoration', ddddd.entity.character.spells.SpellTypes.FIFTH),

            ('Find the Path', ddddd.entity.character.spells.SpellTypes.SIXTH),
            ('Heal', ddddd.entity.character.spells.SpellTypes.SIXTH),
            ('Harm', ddddd.entity.character.spells.SpellTypes.SIXTH),

            ('Plane Shift', ddddd.entity.character.spells.SpellTypes.SEVENTH),
            ('Fire Storm', ddddd.entity.character.spells.SpellTypes.SEVENTH),

            ('Earthquake', ddddd.entity.character.spells.SpellTypes.EIGHTH),

            ('Gate', ddddd.entity.character.spells.SpellTypes.NINTH),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)
        spellcasting = ClericSpellcastingAbility(list_spells_known=casting_spells,
                                                 spell_slots=spells.get_spell_slot_by_level(19),
                                                 num_spells_known=5 + 19 + 10,
                                                 num_cantrips_known=spells.cantrips_by_level(5), cantrips=self.spellcasting.cantrips)
        self.spellcasting = spellcasting

    def _add_level_20_features(self, **kwargs):
        self._append_feature('divine_intervention',
                             feature=feature.Feature(name='Improved Divine Intervention',
                                                     description='At 20th level, your call for intervention succeeds automatically, \
                                                 no roll required.'))

        simple_spell_list = [
            ('Command', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Identify', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Cure Wounds', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Bless', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Healing Word', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Sanctuary', ddddd.entity.character.spells.SpellTypes.FIRST),
            ('Guiding Bolt', ddddd.entity.character.spells.SpellTypes.FIRST),

            ('Enhance Ability', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Lesser Restoration', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Spiritual Weapon', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Augury', ddddd.entity.character.spells.SpellTypes.SECOND),
            ('Suggestion', ddddd.entity.character.spells.SpellTypes.SECOND),

            ('Nondetection', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Speak with Dead', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Tongues', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Bestow Curse', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Spirit Guardians', ddddd.entity.character.spells.SpellTypes.THIRD),
            ('Revivify', ddddd.entity.character.spells.SpellTypes.THIRD),

            ('Banishment', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Arcane Eye', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Confusion', ddddd.entity.character.spells.SpellTypes.FOURTH),
            ('Freedom of Movement', ddddd.entity.character.spells.SpellTypes.FOURTH),

            ('Geas', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Legend Lore', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Scrying', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Flame Strike', ddddd.entity.character.spells.SpellTypes.FIFTH),
            ('Greater Restoration', ddddd.entity.character.spells.SpellTypes.FIFTH),

            ('Find the Path', ddddd.entity.character.spells.SpellTypes.SIXTH),
            ('Heal', ddddd.entity.character.spells.SpellTypes.SIXTH),
            ('Harm', ddddd.entity.character.spells.SpellTypes.SIXTH),

            ('Plane Shift', ddddd.entity.character.spells.SpellTypes.SEVENTH),
            ('Fire Storm', ddddd.entity.character.spells.SpellTypes.SEVENTH),

            ('Earthquake', ddddd.entity.character.spells.SpellTypes.EIGHTH),

            ('Gate', ddddd.entity.character.spells.SpellTypes.NINTH),
            ('True Ressurection', ddddd.entity.character.spells.SpellTypes.NINTH),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)
        spellcasting = ClericSpellcastingAbility(list_spells_known=casting_spells,
                                                 spell_slots=spells.get_spell_slot_by_level(20),
                                                 num_spells_known=5 + 20 + 10,
                                                 num_cantrips_known=spells.cantrips_by_level(5), cantrips=self.spellcasting.cantrips)
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
    def __init__(self, spell_slots, list_spells_known,
                 num_spells_known,
                 num_cantrips_known, cantrips):
        super(ClericSpellcastingAbility, self).__init__(base.AbilityScore.WIS,
                                                        spell_slots, list_spells_known,
                                                        num_cantrips_known=num_cantrips_known, cantrips=cantrips)
        self.num_spells_known = num_spells_known

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
            'knowledge': KnowledgeDomainStrategy(),
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


class KnowledgeDomainStrategy(ClericDomain):

    def add_level_1_features(self, **kwargs):
        new_features = {}
        new_stuff = {'features': new_features}
        return new_stuff

    def add_level_2_features(self, **kwargs):
        new_features = {}
        new_stuff = {'features': new_features}
        return new_stuff

    def add_level_3_features(self, **kwargs):
        new_features = {}
        new_stuff = {'features': new_features}
        return new_stuff

    def add_level_5_features(self, **kwargs):
        new_features = {}
        new_stuff = {'features': new_features}
        return new_stuff

    def add_level_6_features(self, **kwargs):
        new_features = {}
        new_stuff = {'features': new_features}
        return new_stuff

    def add_level_7_features(self, **kwargs):
        new_features = {}
        new_stuff = {'features': new_features}
        return new_stuff

    def add_level_8_features(self, **kwargs):
        new_features = {}
        new_stuff = {'features': new_features}
        return new_stuff

    def add_level_9_features(self, **kwargs):
        new_features = {}
        new_stuff = {'features': new_features}
        return new_stuff

    def add_level_17_features(self, **kwargs):
        new_features = {
            'visions_of_the_past': feature.Feature(name='Visions of the Past',
                                                   description='Starting at 17th level, you can call up \
                                                   visions of the past that relate to an object you hold or your immediate surroundings.')
        }
        new_stuff = {'features': new_features}
        return new_stuff
