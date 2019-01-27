
from ddddd.entity import base
from ddddd.entity.base import AbilityScores, Skills, Languages, SpellTypes
from ddddd.entity.character import spells


class PlayerClass(base.Jsonable):
    """
    A player character's (PC) class.
    This particular feature is going to be modelled by aggregating
    all the class/level combinations to view the PC's class.
    This model reflects how the PHB breaks down the class by level,
    as well as make multiclassing easier to manage.
    i.e. a pure 10th level ranger will have ranger_1, ranger_2,
    ..., ranger_10 objects. Whereas a barbarian 2/druid 2 PC
    will have a total of 4 objects, 2 from each class.
    """
    def __init__(self, name, level, hit_die,
                 proficiencies, saving_throws, skill_proficiencies, features,
                 spellcasting=None):
        self.name = name
        self.level = level
        self.hit_die = hit_die
        self.proficiencies = proficiencies
        self.saving_throws = saving_throws
        self.skills = skill_proficiencies
        self.features = features
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
        }
        return j
    
    @property
    def languages(self):
        if base.LANGUAGES in self.features:
            return self.features[base.LANGUAGES][base.LANGUAGES]
        return []


class PlayerClassFactory(object):
    """
    A class factory. This must be extended to accomodate a specific
    class. This enforces classes to implement features that
    the PC gains upon reaching a specific level.
    """
    def __init__(self):
        pass

    def generate_by_level(self, level, **kwargs):
        if level == 1:
            return self._generate_class_1(**kwargs)
        elif level == 2:
            return self._generate_class_2(**kwargs)
        else:
            print('not a valid level!')
            return None

    def _generate_class_1(self, **kwargs):
        pass

    def _req_class_1(self):
        pass

    def _validate_class_1(self, **kwargs):
        pass

    def _generate_class_2(self, **kwargs):
        pass

    def _req_class_2(self):
        pass

    def _validate_class_2(self, **kwargs):
        pass


class RangerFactory(PlayerClassFactory):
    def _generate_class_1(self, skill_proficiencies=None, favored_enemy=None, languages=None, favored_terrain=None):
        # validation
        self._validate_class_1(skill_proficiencies=skill_proficiencies, favored_enemy=favored_enemy, languages=languages, favored_terrain=favored_terrain)

        def_features = {
            'favored_enemy': {
                base.NAME: 'Favored Enemy',
                base.DESCRIPTION: 'Beginning at 1st level, you have significant experience studying, tracking, hunting, and even talking to a certain type of enemy. ...',
                'enemies': [favored_enemy],
            },
            base.LANGUAGES: {
                base.NAME: 'Favored Enemy Languages',
                base.DESCRIPTION: 'You learn a language that your favored enemy would typically know.',
                base.LANGUAGES: [languages],
            },
            'natural_explorer': {
                base.NAME: 'Natural Explorer',
                base.DESCRIPTION: 'You are particularly familiar with one type of natural environment and are adept at traveling and surviving in such regions. ...',
                'terrains': [favored_terrain]
            },
        }
        return Ranger(level=1,
                      skill_proficiencies=skill_proficiencies,
                      features=def_features,
                      spellcasting=None)

    def _req_class_1(self):
        req = {
            base.SKILL_PROF: {
                base.SKILLS: [Skills.ANIMAL_HANDLING, Skills.ATHLETICS,
                              Skills.INSIGHT, Skills.INVESTIGATION, Skills.NATURE,
                              Skills.PERCEPTION, Skills.STEALTH, Skills.SURVIVAL],
                base.CHOICES: 3,
            },
            'favored_enemy': {
                'enemies': ['aberrations', 'fey', 'elementals', 'plants'],
                base.CHOICES: 1,
            },
            base.LANGUAGES: {
                base.LANGUAGES: Languages.LANGUAGES,
                base.CHOICES: 1,
            },
            'favored_terrain': {
                'terrains': ['forest', 'grassland', 'swamp'],
                base.CHOICES: 1,
            }
        }
        return req
    
    def _validate_class_1(self, **kwargs):
        skill_proficiencies = kwargs[base.SKILL_PROFS]
        if len(skill_proficiencies) != 3:
            raise ValueError('You must pick 3 skill proficiencies!')

        def_skills = set(self._req_class_1()[base.SKILL_PROF][base.SKILLS])
        if not set(skill_proficiencies).issubset(def_skills):
            raise ValueError('You must pick valid skill proficiencies!')

        favored_enemy = kwargs['favored_enemy']
        if not favored_enemy or favored_enemy not in self._req_class_1()['favored_enemy']['enemies']:
            raise ValueError('You must select a favored enemy!')

        languages = kwargs[base.LANGUAGES]
        if not languages:
            raise ValueError('You must select a language!')

        favored_terrain = kwargs['favored_terrain']
        if not favored_terrain or favored_terrain not in self._req_class_1()['favored_terrain']['terrains']:
            raise ValueError('You must select a favored terrain!')
        return True

    def _generate_class_2(self, fighting_style=None):
        # validation
        self._validate_class_2(fighting_style=fighting_style)

        features = {
            'fighting_style': {
                base.NAME: 'Fighting Style',
                base.DESCRIPTION: 'At 2nd level, you adopt a particular style of fighting as your specialty.',
                'style': [fighting_style],
            }
        }

        # TODO make this a bit more elegant...
        list_spells = []
        simple_spell_list = [
            ('Hunters Mark', 1),
            ('Animal Friendship', 1),
        ]
        for name, level in simple_spell_list:
            list_spells.append(spells.generate_simple_spell(name, level))
        spellcasting = spells.RangerSpellcastingAbility(spellcasting_ability=AbilityScores.WIS,
                                                        list_spells_known=list_spells,
                                                        spell_slots={SpellTypes.FIRST: 2},
                                                        num_spells_known=2)
        return Ranger(level=2, skill_proficiencies=[], features=features, spellcasting=spellcasting)

    def _req_class_2(self):
        req = {
            'fighting_style': {
                'styles': ['archery', 'defense', 'dueling', 'two_weapon_fighting'],
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
    
    def _validate_class_2(self, **kwargs):
        fighting_style = kwargs['fighting_style']
        if fighting_style[0] not in self._req_class_2()['fighting_style']['styles']:
            raise ValueError('You must pick a fighting style!')

        return True


class Ranger(PlayerClass):
    def __init__(self, level, skill_proficiencies, features, spellcasting):
        super(Ranger, self).__init__(name='Ranger',
                                     level=level,
                                     hit_die=10,
                                     proficiencies={
                                         base.ARMOR: ['light', 'medium', 'shields'],
                                         base.WEAPONS: ['simple', 'martial'],
                                         base.TOOLS: [],
                                     },
                                     saving_throws=[AbilityScores.STR, AbilityScores.DEX],
                                     skill_proficiencies=skill_proficiencies,
                                     features=features,
                                     spellcasting=spellcasting)
