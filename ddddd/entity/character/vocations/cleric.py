from ddddd.entity import base
from ddddd.entity.base import AbilityScore, Skills, Languages, SpellTypes
from ddddd.entity.character import spells, trait
from ddddd.entity.character.vocation import Vocation


class Cleric(Vocation):
    FAVORED_ENEMY = 'favored_enemy'
    ENEMIES = 'enemies'
    NATURAL_EXPLORER = 'natural_explorer'
    TERRAINS = 'terrains'
    FIGHTING_STYLE = 'fighting_style'
    STYLES = 'styles'

    def __init__(self, skill_proficiencies, languages, cantrips):
        def_features = [
            trait.Trait(name='Divine Domain',
                        description='You have chosen to worship Ioun, goddess of knowledge. \
                                    Your divine domain is the Knowledge Domain.'),
            trait.Trait(name='Blessings of Knowledge',
                        description='At 1st level, you learn two languages of your choice. \
                        You also become proficient in your choice of two of the following skills: \
                        Arcana, History, Nature, or Religion. Your proficiency bonus is doubled \
                        for any ability check you make that uses either of those skills.'),
            languages,
        ]

        simple_spell_list = [
            ('Command', base.SpellTypes.FIRST),
            ('Identify', base.SpellTypes.FIRST),
            ('Cure Wounds', base.SpellTypes.FIRST),
            ('Bless', base.SpellTypes.FIRST),
            ('Healing Word', base.SpellTypes.FIRST),
            ('Sanctuary', base.SpellTypes.FIRST),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)
        spellcasting = ClericSpellcastingAbility(spellcasting_ability=AbilityScore.WIS,
                                                 list_spells_known=casting_spells,
                                                 spell_slots={
                                                     SpellTypes.FIRST: 2
                                                 },
                                                 num_spells_known=3 + 1 + 2,
                                                 num_cantrips_known=3, cantrips=cantrips)

        super(Cleric, self).__init__(name='Cleric',
                                     level=1,
                                     hit_die=8,
                                     proficiencies={
                                         base.ARMOR_PROFICIENCY: trait.ArmorProficiency(name='Armor Proficiency',
                                                                                        proficiencies=['light',
                                                                                                       'medium',
                                                                                                       'shields']),
                                         base.WEAPON_PROFICIENCY: trait.WeaponProficiency(name='Weapon Proficiency',
                                                                                          proficiencies=['simple']),
                                     },
                                     saving_throws=[AbilityScore.WIS, AbilityScore.CHA],
                                     skill_proficiencies=skill_proficiencies,
                                     features=def_features,
                                     spellcasting=spellcasting,
                                     asi=None)

    def _level_1_requirements(self):
        return {}

    def _level_2_requirements(self):
        req = {}
        return req

    def _add_level_2_features(self, **kwargs):
        self.features.append(
            trait.Trait(name='Channel Divinity',
                        description='At 2nd level, you gain the ability to channel divine energy directly \
                        from your deity, using that energy to fuel magical effects. When you finish a short \
                        or long rest, you regain your expended uses.')
        )
        self.features.append(
            trait.Trait(name='Channel Divinity: Turn Undead',
                        description='As an action, you present your holy symbol \
                        and speak a prayer censuring the undead.')
        )
        self.features.append(
            trait.Trait(name='Channel Divinity: Knowledge of the Ages',
                        description='Starting at 2nd level, you can use your Channel Divinity to tap into \
                        a divine well of knowledge. As an action, you choose one skill or tool. \
                        For 10 minutes, you have proficiency with the chosen skill or tool.')
        )

        simple_spell_list = [
            ('Command', base.SpellTypes.FIRST),
            ('Identify', base.SpellTypes.FIRST),
            ('Cure Wounds', base.SpellTypes.FIRST),
            ('Bless', base.SpellTypes.FIRST),
            ('Healing Word', base.SpellTypes.FIRST),
            ('Inflict Wounds', base.SpellTypes.FIRST),
            ('Sanctuary', base.SpellTypes.FIRST),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)
        spellcasting = ClericSpellcastingAbility(spellcasting_ability=AbilityScore.WIS,
                                                 list_spells_known=casting_spells,
                                                 spell_slots={
                                                     SpellTypes.FIRST: 3
                                                 },
                                                 num_spells_known=3 + 2 + 2,
                                                 num_cantrips_known=3, cantrips=self.spellcasting.cantrips)
        self.spellcasting = spellcasting

    def _level_3_requirements(self):
        req = {}
        return req

    def _add_level_3_features(self, **kwargs):
        simple_spell_list = [
            ('Command', base.SpellTypes.FIRST),
            ('Identify', base.SpellTypes.FIRST),
            ('Cure Wounds', base.SpellTypes.FIRST),
            ('Bless', base.SpellTypes.FIRST),
            ('Healing Word', base.SpellTypes.FIRST),
            ('Sanctuary', base.SpellTypes.FIRST),

            ('Enhance Ability', base.SpellTypes.SECOND),
            ('Lesser Restoration', base.SpellTypes.SECOND),
            ('Augury', base.SpellTypes.SECOND),
            ('Suggestion', base.SpellTypes.SECOND),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)
        spellcasting = ClericSpellcastingAbility(spellcasting_ability=AbilityScore.WIS,
                                                 list_spells_known=casting_spells,
                                                 spell_slots={
                                                     SpellTypes.FIRST: 4,
                                                     SpellTypes.SECOND: 2
                                                 },
                                                 num_spells_known=3 + 3 + 4,
                                                 num_cantrips_known=3, cantrips=self.spellcasting.cantrips)
        self.spellcasting = spellcasting

    def _level_4_requirements(self):
        req = {
            'ability_score_increase': {
                'name': 'Ability Score Increase',
                'description': 'You can increase one ability score of your choice by 2, or you can increase two Ability Scores of your choice by 1.',
            },
        }
        return req

    def _add_level_4_features(self, **kwargs):
        ability_score_increase = kwargs['ability_score_increase_4']
        for ability in ability_score_increase.keys():
            if ability not in self.asi:
                self.asi[ability] = ability_score_increase[ability]
            else:
                self.asi[ability] = self.asi[ability].combine(ability_score_increase[ability])

        new_cantrip = kwargs['cantrip_4']
        self.spellcasting.cantrips.append(new_cantrip)
        simple_spell_list = [
            ('Command', base.SpellTypes.FIRST),
            ('Identify', base.SpellTypes.FIRST),
            ('Cure Wounds', base.SpellTypes.FIRST),
            ('Bless', base.SpellTypes.FIRST),
            ('Healing Word', base.SpellTypes.FIRST),
            ('Sanctuary', base.SpellTypes.FIRST),
            ('Guiding Bolt', base.SpellTypes.FIRST),

            ('Enhance Ability', base.SpellTypes.SECOND),
            ('Lesser Restoration', base.SpellTypes.SECOND),
            ('Augury', base.SpellTypes.SECOND),
            ('Suggestion', base.SpellTypes.SECOND),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)
        spellcasting = ClericSpellcastingAbility(spellcasting_ability=AbilityScore.WIS,
                                                 list_spells_known=casting_spells,
                                                 spell_slots={
                                                     SpellTypes.FIRST: 4,
                                                     SpellTypes.SECOND: 3
                                                 },
                                                 num_spells_known=4 + 4 + 4,
                                                 num_cantrips_known=4, cantrips=self.spellcasting.cantrips)
        self.spellcasting = spellcasting

    def _level_5_requirements(self):
        req = {
            base.SPELLCASTING: {
                base.SPELLCASTING_ABILITY: AbilityScore.WIS,
                base.NUM_SPELLS_KNOWN: 4,
                base.SPELL_SLOTS: {
                    SpellTypes.FIRST: 4,
                    SpellTypes.SECOND: 2,
                }
            },
        }
        return req

    def _add_level_5_features(self, **kwargs):
        self.features.append(
            trait.Trait(name='Channel Divinity: Destroy Undead',
                        description='Starting at 5th level, when an undead fails its saving throw \
                        against your Turn Undead feature, the creature is instantly destroyed \
                        if its challenge rating is at or below CR 1/2.')
        )

        # TODO work on the mechanic to override stuff
        self.features.append(
            trait.Trait(name='Channel Divinity (2/rest)',
                        description='')
        )

        simple_spell_list = [
            ('Command', base.SpellTypes.FIRST),
            ('Identify', base.SpellTypes.FIRST),
            ('Cure Wounds', base.SpellTypes.FIRST),
            ('Bless', base.SpellTypes.FIRST),
            ('Healing Word', base.SpellTypes.FIRST),
            ('Sanctuary', base.SpellTypes.FIRST),
            ('Guiding Bolt', base.SpellTypes.FIRST),

            ('Enhance Ability', base.SpellTypes.SECOND),
            ('Lesser Restoration', base.SpellTypes.SECOND),
            ('Spiritual Weapon', base.SpellTypes.SECOND),
            ('Augury', base.SpellTypes.SECOND),
            ('Suggestion', base.SpellTypes.SECOND),

            ('Nondetection', base.SpellTypes.THIRD),
            ('Speak with Dead', base.SpellTypes.THIRD),
            ('Tongues', base.SpellTypes.THIRD),
        ]
        casting_spells = spells.generate_simple_spell_list(simple_spell_list)
        spellcasting = ClericSpellcastingAbility(spellcasting_ability=AbilityScore.WIS,
                                                 list_spells_known=casting_spells,
                                                 spell_slots={
                                                     SpellTypes.FIRST: 4,
                                                     SpellTypes.SECOND: 3,
                                                     SpellTypes.THIRD: 3,
                                                 },
                                                 num_spells_known=4 + 5 + 6,
                                                 num_cantrips_known=4, cantrips=self.spellcasting.cantrips)
        self.spellcasting = spellcasting

    def _add_level_6_features(self, **kwargs):
        return {}

    def _add_level_7_features(self, **kwargs):
        return {}

    def _add_level_8_features(self, **kwargs):
        self._aggregate_ability_score_increase(kwargs['ability_score_increase_8'])

    def _add_level_9_features(self, **kwargs):
        return {}

    def _add_level_10_features(self, **kwargs):
        return {}

    def _add_level_11_features(self, **kwargs):
        return {}

    def _add_level_12_features(self, **kwargs):
        self._aggregate_ability_score_increase(kwargs['ability_score_increase_12'])

    def _add_level_13_features(self, **kwargs):
        return {}

    def _add_level_14_features(self, **kwargs):
        return {}

    def _add_level_15_features(self, **kwargs):
        return {}

    def _add_level_16_features(self, **kwargs):
        self._aggregate_ability_score_increase(kwargs['ability_score_increase_16'])

    def _add_level_17_features(self, **kwargs):
        return {}

    def _add_level_18_features(self, **kwargs):
        return {}

    def _add_level_19_features(self, **kwargs):
        self._aggregate_ability_score_increase(kwargs['ability_score_increase_19'])

    def _add_level_20_features(self, **kwargs):
        return {}

    def _aggregate_ability_score_increase(self, asi):
        for ability in asi.keys():
            if ability not in self.asi:
                self.asi[ability] = asi[ability]
            else:
                self.asi[ability] = self.asi[ability].combine(asi[ability])


class ClericSpellcastingAbility(spells.SpellcastingAbility):
    def __init__(self, spellcasting_ability,
                 spell_slots, list_spells_known,
                 num_spells_known,
                 num_cantrips_known, cantrips):
        super(ClericSpellcastingAbility, self).__init__(spellcasting_ability,
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
