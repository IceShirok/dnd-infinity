from ddddd.entity import base
from ddddd.entity.base import AbilityScore, Skills, Languages, SpellTypes
from ddddd.entity.character import spells, feature
from ddddd.entity.character.vocation import Vocation


class Ranger(Vocation):
    FAVORED_ENEMY = 'favored_enemy'
    ENEMIES = 'enemies'
    NATURAL_EXPLORER = 'natural_explorer'
    TERRAINS = 'terrains'
    FIGHTING_STYLE = 'fighting_style'
    STYLES = 'styles'

    def __init__(self, skill_proficiencies, favored_enemy=None, languages=None, favored_terrain=None):
        def_features = {
            'favored_enemy': FavoredEnemy([favored_enemy]),
            'favored_enemy_languages': feature.LanguagesKnown(languages=[languages], name='Favored Enemy Languages',
                                                              description='You learn a language that your favored enemy would typically know.'),
            'natural_explorer': NaturalExplorer([favored_terrain]),
        }

        super(Ranger, self).__init__(name='Ranger',
                                     level=1,
                                     hit_die=10,
                                     proficiencies={
                                         base.ARMOR_PROFICIENCY: feature.ArmorProficiency(name='Armor Proficiency',
                                                                                          proficiencies=['light',
                                                                                                       'medium',
                                                                                                       'shields']),
                                         base.WEAPON_PROFICIENCY: feature.WeaponProficiency(name='Weapon Proficiency',
                                                                                            proficiencies=['simple',
                                                                                                         'martial']),
                                     },
                                     saving_throws=[AbilityScore.STR, AbilityScore.DEX],
                                     skill_proficiencies=skill_proficiencies,
                                     features=def_features,
                                     spellcasting=None,
                                     asi=None)

    def _add_level_2_features(self, **kwargs):
        fighting_style = kwargs['fighting_style']
        self._append_feature('fighting_style',
                             feature=feature.Feature(name='Fighting Style',
                                                     description='At 2nd level, you adopt a particular style of fighting \
                                                 as your specialty. {}'.format(fighting_style)))

        # TODO make this a bit more elegant...
        list_spells = []
        simple_spell_list = [
            ('Hunters Mark', base.SpellTypes.FIRST),
            ('Animal Friendship', base.SpellTypes.FIRST),
        ]
        for name, level in simple_spell_list:
            list_spells.append(spells.generate_simple_spell(name, level))
        self.spellcasting = RangerSpellcastingAbility(spellcasting_ability=AbilityScore.WIS,
                                                      casting_spells=list_spells,
                                                      spell_slots={SpellTypes.FIRST: 2},
                                                      num_spells_known=2)

    def _add_level_3_features(self, **kwargs):
        self._append_feature('primeval_awareness',
                             feature=feature.Feature(name='Primeval Awareness',
                                                     description='Beginning at 3rd level, you can use your action and expend one Ranger spell slot \
                                                 to focus your awareness on the region around you..'))

        archetype_feature = kwargs['archetype_feature']
        # TODO clean up the martial specialized features
        self._append_feature('ranger_archetype',
                             feature=feature.Feature(name='Ranger Archetype',
                                                     description='Emulating the Hunter archetype means accepting your place as a bulwark \
                                                 between civilization and the terrors of The Wilderness.'.format(archetype_feature)))

        # TODO make this a bit more elegant...
        list_spells = []
        simple_spell_list = [
            ('Hunters Mark', base.SpellTypes.FIRST),
            ('Animal Friendship', base.SpellTypes.FIRST),
            ('Longstrider', base.SpellTypes.FIRST),
        ]
        for name, level in simple_spell_list:
            list_spells.append(spells.generate_simple_spell(name, level))
        self.spellcasting = RangerSpellcastingAbility(spellcasting_ability=AbilityScore.WIS,
                                                      casting_spells=list_spells,
                                                      spell_slots={SpellTypes.FIRST: 3},
                                                      num_spells_known=3)

    def _add_level_4_features(self, **kwargs):
        self._aggregate_asi_or_feat(kwargs, level=4)

    def _add_level_5_features(self, **kwargs):
        self._append_feature('extra_attack',
                             feature=feature.Feature(name='Extra Attack',
                                                     description='Beginning at 5th level, you can Attack twice, instead of once, \
                                                    whenever you take the Attack action on Your Turn.'))

        # TODO make this a bit more elegant...
        list_spells = []
        simple_spell_list = [
            ('Hunters Mark', base.SpellTypes.FIRST),
            ('Animal Friendship', base.SpellTypes.FIRST),
            ('Longstrider', base.SpellTypes.FIRST),
            ('Pass without Trace', base.SpellTypes.SECOND),
        ]
        for name, level in simple_spell_list:
            list_spells.append(spells.generate_simple_spell(name, level))
        self.spellcasting = RangerSpellcastingAbility(spellcasting_ability=AbilityScore.WIS,
                                                      casting_spells=list_spells,
                                                      spell_slots={SpellTypes.FIRST: 4, SpellTypes.SECOND: 2},
                                                      num_spells_known=4)

    def _add_level_6_features(self, **kwargs):
        return {}

    def _add_level_7_features(self, **kwargs):
        return {}

    def _add_level_8_features(self, **kwargs):
        return {}

    def _add_level_9_features(self, **kwargs):
        return {}

    def _add_level_10_features(self, **kwargs):
        return {}

    def _add_level_11_features(self, **kwargs):
        return {}

    def _add_level_12_features(self, **kwargs):
        return {}

    def _add_level_13_features(self, **kwargs):
        return {}

    def _add_level_14_features(self, **kwargs):
        return {}

    def _add_level_15_features(self, **kwargs):
        return {}

    def _add_level_16_features(self, **kwargs):
        return {}

    def _add_level_17_features(self, **kwargs):
        return {}

    def _add_level_18_features(self, **kwargs):
        return {}

    def _add_level_19_features(self, **kwargs):
        return {}

    def _add_level_20_features(self, **kwargs):
        return {}


class RangerSpellcastingAbility(spells.SpellcastingAbility):
    def __init__(self, spellcasting_ability,
                 spell_slots, casting_spells,
                 num_spells_known):
        super(RangerSpellcastingAbility, self).__init__(spellcasting_ability,
                                                        spell_slots, casting_spells)
        self.num_spells_known = num_spells_known
        self._verify()

    def _verify(self):
        super(RangerSpellcastingAbility, self)._verify()
        if len(self.casting_spells) != self.num_spells_known:
            raise ValueError('Must have {} spells but inputted {} spells!'.format(self.num_spells_known,
                                                                                  len(self.casting_spells)))


###############################
# Ranger-specific traits
###############################

class FavoredEnemy(feature.Feature):
    def __init__(self, favored_enemies):
        desc = 'Beginning at 1st level, you have significant experience studying, tracking, \
                hunting, and even talking to a certain type of enemy.'
        final_desc = '{} Your favored enemies are {}.'.format(desc, feature.format_list_as_english_string(favored_enemies))
        super(FavoredEnemy, self).__init__(name='Favored Enemy',
                                           description=final_desc)
        self.favored_enemies = favored_enemies


class NaturalExplorer(feature.Feature):
    def __init__(self, favored_terrains):
        desc = 'You are particularly familiar with one type of natural environment \
                and are adept at traveling and surviving in such regions.'
        final_desc = '{} Your favored terrains are {}.'.format(desc, feature.format_list_as_english_string(favored_terrains))
        super(NaturalExplorer, self).__init__(name='Natural Explorer',
                                              description=final_desc)
        self.favored_terrains = favored_terrains
