
import abc

from ddddd.entity import base
from ddddd.entity.base import AbilityScores, Skills, Languages, SpellTypes
from ddddd.entity.character import spells


class PlayerClass(base.Jsonable, metaclass=abc.ABCMeta):
    """
    A representation of a player character (PC) class
    for a particular class/level combination. This particular
    class is fairly dumb.
    """
    def __init__(self, name, level, hit_die,
                 proficiencies, saving_throws, skill_proficiencies, features, asi,
                 spellcasting=None):
        self.name = name
        self.level = level
        self.hit_die = hit_die
        self.proficiencies = proficiencies
        self.saving_throws = saving_throws
        self.skills = skill_proficiencies
        self.features = features
        self.asi = asi if asi else []
        self.spellcasting = spellcasting

    def __json__(self):
        spellcasting_p = self.spellcasting
        if spellcasting_p:
            spellcasting_p = spellcasting_p.__json__()
        j = {
            base.CLASS: self.name,
            base.LEVEL: self.level,
            base.HIT_DIE: 'd{}'.format(self.hit_die),
            base.PROFICIENCIES: self.proficiencies,
            base.SAVING_THROWS: self.saving_throws,
            base.SKILLS: self.skills,
            base.FEATURES: self.features,
            base.SPELLCASTING: spellcasting_p,
            'ability_score_increase': self.asi,
        }
        return j
    
    @property
    def languages(self):
        if base.LANGUAGES in self.features:
            return self.features[base.LANGUAGES][base.LANGUAGES]
        return []

    def get_requirements(self, level):
        if level == 1:
            return self._level_1_requirements()
        elif level == 2:
            return self._level_2_requirements()
        elif level == 3:
            return self._level_3_requirements()
        elif level == 4:
            return self._level_4_requirements()
        elif level == 5:
            return self._level_5_requirements()
        else:
            raise ValueError('Invalid level!')

    @abc.abstractmethod
    def _level_1_requirements(self):
        return {}

    @abc.abstractmethod
    def _level_2_requirements(self):
        return {}

    @abc.abstractmethod
    def _level_3_requirements(self):
        return {}

    @abc.abstractmethod
    def _level_4_requirements(self):
        return {}

    @abc.abstractmethod
    def _level_5_requirements(self):
        return {}

    def level_to(self, level, **kwargs):
        if level <= self.level:
            raise ValueError('This class is already larger than requested!')

        start, end = (self.level+1, level+1)
        for i in range(start, end):
            self.level = i
            if i == 2:
                self._add_level_2_features(**kwargs)
            elif i == 3:
                self._add_level_3_features(**kwargs)
            elif i == 4:
                self._add_level_4_features(**kwargs)
            elif i == 5:
                self._add_level_5_features(**kwargs)
            else:
                raise ValueError('Invalid level!')

    @abc.abstractmethod
    def _add_level_2_features(self, **kwargs):
        return {}

    @abc.abstractmethod
    def _add_level_3_features(self, **kwargs):
        return {}

    @abc.abstractmethod
    def _add_level_4_features(self, **kwargs):
        return {}

    @abc.abstractmethod
    def _add_level_5_features(self, **kwargs):
        return {}


class Ranger(PlayerClass):
    FAVORED_ENEMY = 'favored_enemy'
    ENEMIES = 'enemies'
    NATURAL_EXPLORER = 'natural_explorer'
    TERRAINS = 'terrains'
    FIGHTING_STYLE = 'fighting_style'
    STYLES = 'styles'

    def __init__(self, skill_proficiencies, favored_enemy=None, languages=None, favored_terrain=None):
        def_features = {
            self.FAVORED_ENEMY: {
                base.NAME: 'Favored Enemy',
                base.DESCRIPTION: 'Beginning at 1st level, you have significant experience studying, tracking, hunting, and even talking to a certain type of enemy. ...',
                self.ENEMIES: [favored_enemy],
            },
            base.LANGUAGES: {
                base.NAME: 'Favored Enemy Languages',
                base.DESCRIPTION: 'You learn a language that your favored enemy would typically know.',
                base.LANGUAGES: [languages],
            },
            self.NATURAL_EXPLORER: {
                base.NAME: 'Natural Explorer',
                base.DESCRIPTION: 'You are particularly familiar with one type of natural environment and are adept at traveling and surviving in such regions. ...',
                self.TERRAINS: [favored_terrain]
            },
        }
        super(Ranger, self).__init__(name='Ranger',
                                     level=1,
                                     hit_die=10,
                                     proficiencies={
                                         base.ARMOR: ['light', 'medium', 'shields'],
                                         base.WEAPONS: ['simple', 'martial'],
                                         base.TOOLS: [],
                                     },
                                     saving_throws=[AbilityScores.STR, AbilityScores.DEX],
                                     skill_proficiencies=skill_proficiencies,
                                     features=def_features,
                                     spellcasting=None,
                                     asi=None)

    def _level_1_requirements(self):
        return {
            base.SKILL_PROF: {
                base.SKILLS: [Skills.ANIMAL_HANDLING, Skills.ATHLETICS,
                              Skills.INSIGHT, Skills.INVESTIGATION, Skills.NATURE,
                              Skills.PERCEPTION, Skills.STEALTH, Skills.SURVIVAL],
                base.CHOICES: 3,
            },
            self.FAVORED_ENEMY: {
                self.ENEMIES: ['aberrations', 'fey', 'elementals', 'plants'],
                base.CHOICES: 1,
            },
            base.LANGUAGES: {
                base.LANGUAGES: Languages.LANGUAGES,
                base.CHOICES: 1,
            },
            self.NATURAL_EXPLORER: {
                self.TERRAINS: ['forest', 'grassland', 'swamp'],
                base.CHOICES: 1,
            }
        }

    def _level_2_requirements(self):
        req = {
            self.FIGHTING_STYLE: {
                self.STYLES: ['archery', 'defense', 'dueling', 'two_weapon_fighting'],
                base.CHOICES: 1,
            },
            base.SPELLCASTING: {
                base.SPELLCASTING_ABILITY: AbilityScores.WIS,
                base.NUM_SPELLS_KNOWN: 2,
                base.SPELL_SLOTS: {
                    SpellTypes.FIRST: 2
                }
            }
        }
        return req

    def _add_level_2_features(self, **kwargs):
        fighting_style = kwargs['fighting_style']
        self.features[self.FIGHTING_STYLE] = {
            base.NAME: 'Fighting Style',
            base.DESCRIPTION: 'At 2nd level, you adopt a particular style of fighting as your specialty.',
            self.STYLES: [fighting_style],
        }

        # TODO make this a bit more elegant...
        list_spells = []
        simple_spell_list = [
            ('Hunters Mark', base.SpellTypes.FIRST),
            ('Animal Friendship', base.SpellTypes.FIRST),
        ]
        for name, level in simple_spell_list:
            list_spells.append(spells.generate_simple_spell(name, level))
        self.spellcasting = spells.RangerSpellcastingAbility(spellcasting_ability=AbilityScores.WIS,
                                                             list_spells_known=list_spells,
                                                             spell_slots={SpellTypes.FIRST: 2},
                                                             num_spells_known=2)

    def _level_3_requirements(self):
        req = {
            'archetype_feature': {
                'name': 'Hunter',
                'features': ['colossus_slayer', 'giant_killer', 'horde_breaker'],
                base.CHOICES: 1,
            },
            base.SPELLCASTING: {
                base.SPELLCASTING_ABILITY: AbilityScores.WIS,
                base.NUM_SPELLS_KNOWN: 3,
                base.SPELL_SLOTS: {
                    SpellTypes.FIRST: 3
                }
            }
        }
        return req

    def _add_level_3_features(self, **kwargs):
        self.features['primeval_awareness'] = {
            base.NAME: 'Primeval Awareness',
            base.DESCRIPTION: 'Beginning at 3rd level, you can use your action and expend one Ranger spell slot to focus your awareness on the region around you..',
        }

        archetype_feature = kwargs['archetype_feature']
        self.features['archetype_feature'] = {
            base.NAME: 'Ranger Archetype',
            base.DESCRIPTION: 'Emulating the Hunter archetype means accepting your place as a bulwark between civilization and the terrors of The Wilderness.',
            'archetype_feature': archetype_feature,
        }

        # TODO make this a bit more elegant...
        list_spells = []
        simple_spell_list = [
            ('Hunters Mark', base.SpellTypes.FIRST),
            ('Animal Friendship', base.SpellTypes.FIRST),
            ('Longstrider', base.SpellTypes.FIRST),
        ]
        for name, level in simple_spell_list:
            list_spells.append(spells.generate_simple_spell(name, level))
        self.spellcasting = spells.RangerSpellcastingAbility(spellcasting_ability=AbilityScores.WIS,
                                                             list_spells_known=list_spells,
                                                             spell_slots={SpellTypes.FIRST: 3},
                                                             num_spells_known=3)

    def _level_4_requirements(self):
        req = {
            'ability_score_increase': {
                'name': 'Ability Score Increase',
                'description': 'You can increase one ability score of your choice by 2, or you can increase two Ability Scores of your choice by 1.',
            },
        }
        return req

    def _add_level_4_features(self, **kwargs):
        ability_score_increase = kwargs['ability_score_increase']
        self.asi.append(ability_score_increase)

    def _level_5_requirements(self):
        req = {
            base.SPELLCASTING: {
                base.SPELLCASTING_ABILITY: AbilityScores.WIS,
                base.NUM_SPELLS_KNOWN: 4,
                base.SPELL_SLOTS: {
                    SpellTypes.FIRST: 4,
                    SpellTypes.SECOND: 2,
                }
            },
        }
        return req

    def _add_level_5_features(self, **kwargs):
        self.features['extra_attack'] = {
            base.NAME: 'Extra Attack',
            base.DESCRIPTION: 'Beginning at 5th level, you can Attack twice, instead of once, whenever you take the Attack action on Your Turn.',
        }

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
        self.spellcasting = spells.RangerSpellcastingAbility(spellcasting_ability=AbilityScores.WIS,
                                                             list_spells_known=list_spells,
                                                             spell_slots={SpellTypes.FIRST: 4, SpellTypes.SECOND: 2},
                                                             num_spells_known=4)
