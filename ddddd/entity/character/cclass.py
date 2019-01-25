
from ddddd.entity import ability_score, proficiency, language
from ddddd.entity.character.spells import SpellcastingAbility

CLASS = 'class'
LEVEL = 'level'
HIT_DIE = 'hit_die'
PROFICIENCIES = 'proficiencies'
SAVING_THROWS = 'saving_throws'
SKILLS = 'skills'
FEATURES = 'features'
SPELLCASTING = 'spellcasting'

LANGUAGES = 'languages'
SKILL_PROF = 'skill_proficiency'
SKILL_PROFS = 'skill_proficiencies'

WEAPONS = 'weapons'
WEAPON_PROFICIENCY = 'weapon_proficiency'
ARMOR = 'armor'
TOOLS = 'tools'
TOOL_PROFICIENCY = 'tool_proficiency'

NAME = 'name'
DESCRIPTION = 'description'
CHOICES = 'choices'


class PlayerClass(object):
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
                CLASS: self.name,
                LEVEL: self.level,
                HIT_DIE: 'd{}'.format(self.hit_die),
                PROFICIENCIES: self.proficiencies,
                SAVING_THROWS: self.saving_throws,
                SKILLS: self.skills,
                FEATURES: self.features,
                SPELLCASTING: spellcasting_p,
            }
        return j
    
    @property
    def languages(self):
        if LANGUAGES in self.features:
            return self.features[LANGUAGES][LANGUAGES]
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
                    NAME: 'Favored Enemy',
                    DESCRIPTION: 'Beginning at 1st level, you have significant experience studying, tracking, hunting, and even talking to a certain type of enemy. ...',
                    'enemies': [favored_enemy],
                },
                LANGUAGES: {
                    NAME: 'Favored Enemy Languages',
                    DESCRIPTION: 'You learn a language that your favored enemy would typically know.',
                    LANGUAGES: [languages],
                },
                'natural_explorer': {
                    NAME: 'Natural Explorer',
                    DESCRIPTION: 'You are particularly familiar with one type of natural environment and are adept at traveling and surviving in such regions. ...',
                    'terrains': [favored_terrain]
                },
        }
        return Ranger(level=1,
                      skill_proficiencies=skill_proficiencies,
                      features=def_features,
                      spellcasting=None)

    def _req_class_1(self):
        req = {
            SKILL_PROF: {
                SKILLS: [proficiency.ANIMAL_HANDLING, proficiency.ATHLETICS, proficiency.INSIGHT, proficiency.INVESTIGATION, proficiency.NATURE, proficiency.PERCEPTION, proficiency.STEALTH, proficiency.SURVIVAL],
                CHOICES: 3,
            },
            'favored_enemy': {
                'enemies': ['aberrations', 'fey', 'elementals', 'plants'],
                CHOICES: 1,
            },
            LANGUAGES: {
                LANGUAGES: language.LANGUAGES,
                CHOICES: 1,
            },
            'favored_terrain': {
                'terrains': ['forest', 'grassland', 'swamp'],
                CHOICES: 1,
            }
        }
        return req
    
    def _validate_class_1(self, **kwargs):
        skill_proficiencies = kwargs[SKILL_PROFS]
        if len(skill_proficiencies) != 3:
            raise ValueError('You must pick 3 skill proficiencies!')

        def_skills = set(self._req_class_1()[SKILL_PROF][SKILLS])
        if not set(skill_proficiencies).issubset(def_skills):
            raise ValueError('You must pick valid skill proficiencies!')

        favored_enemy = kwargs['favored_enemy']
        if not favored_enemy or favored_enemy not in self._req_class_1()['favored_enemy']['enemies']:
            raise ValueError('You must select a favored enemy!')

        languages = kwargs[LANGUAGES]
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
                NAME: 'Fighting Style',
                DESCRIPTION: 'At 2nd level, you adopt a particular style of fighting as your specialty.',
                'style': [fighting_style],
            }
        }

        # TODO make this a bit more elegant...
        spellcasting = SpellcastingAbility(list_spells_known=['hunters_mark', 'cure_wounds'],
                                           spell_slots={"1st": 2})
        return Ranger(level=2, skill_proficiencies=[], features=features, spellcasting=spellcasting)

    def _req_class_2(self):
        req = {
                'fighting_style': {
                    'styles': ['archery', 'defense', 'dueling', 'two_weapon_fighting'],
                    CHOICES: 1,
                },
                SPELLCASTING: {
                    'spellcasting_ability': ability_score.WIS,
                    'spells_known': 2,
                    'spell_slots': {
                        '1st': 2
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
                                         ARMOR: ['light', 'medium', 'shields'],
                                         WEAPONS: ['simple', 'martial'],
                                         TOOLS: [],
                                     },
                                     saving_throws=[ability_score.STR, ability_score.DEX],
                                     skill_proficiencies=skill_proficiencies,
                                     features=features,
                                     spellcasting=spellcasting)
