
import math

from base import Jsonable


"""
A player character (PC) base will consist of the PC's name,
base ability scores, and level by experience. Features that
do not change with certain PC features (race, class, background)
and cannot be derived by other features (i.e. proficiency bonus)
are put in this class.
Why level by experience and not by class? I'm thinking a little
too far ahead, but it's because of multiclassing.
"""
class PlayerBase(Jsonable):

    def __init__(self, name, _str, _dex, _con, _int, _wis, _cha, level=1):
        self.name = name

        self._str = _str
        self._dex = _dex
        self._con = _con
        self._int = _int
        self._wis = _wis
        self._cha = _cha

        self.level = level

    @property
    def ability_scores(self):
        """
        Return the base ability scores.
        """
        return {
                    'STR': self._str,
                    'DEX': self._dex,
                    'CON': self._con,
                    'INT': self._int,
                    'WIS': self._wis,
                    'CHA': self._cha,
                }


    def __json__(self):
        j = {
                'name': self.name,
                'base_ability_scores': self.ability_scores,
                'level': self.level,
                'proficiency_bonus': self.proficiency_bonus,
            }
        return j

    @property
    def proficiency_bonus(self):
        """
        Return the proficiency bonus of the PC.
        Proficiency bonus is based on a character's level.
        TODO fix the formula
        """
        return math.floor((self.level + 3) / 4) + 1


"""
Common functions
"""

def _modifier(score):
    # Calculates the ability modifier
    return math.floor((score-10)/2)

def _modifier_p(score):
    # Calculates and returns a prettified ability modifier score
    mod = _modifier(score)
    if mod > 0:
        return '+{}'.format(mod)
    else:
        return str(mod)

SKILL_PROFICIENCIES = {
    'STR': ['athletics'],
    'DEX': ['acrobatics', 'sleight_of_hand', 'stealth'],
    'CON': [],
    'INT': ['arcana', 'history', 'investigation', 'nature', 'religion'],
    'WIS': ['animal_handling', 'insight', 'medicine', 'perception', 'survival'],
    'CHA': ['deception', 'intimidation', 'performance', 'persuasion'],
}


"""
A player character (PC) in D&D.
A PC consists of some base characteristics, a race, a class, and
a background.
"""
class PlayerCharacter(Jsonable):
    def __init__(self, base, race=None, classes=None, background=None):
        self.base = base
        self.race = race
        self.classes = classes
        self.background = background
    
    @property
    def name(self):
      return self.base.name
    
    @property
    def race_name(self):
      return self.race.name
    
    @property
    def class_name(self):
        # TODO maybe this will be aggregated to a class/level thing
        # this is more important with multiclassing so we can delay this
        return self.classes[0].name
    
    @property
    def level(self):
      return self.base.level
    
    @property
    def background_name(self):
      return self.background.name
    
    @property
    def proficiency_bonus(self):
        return self.base.proficiency_bonus
    
    @property
    def speed(self):
        return self.race.speed
        
    @property
    def size(self):
      return self.race.size

    @property
    def ability_scores(self):
        # Calculate the scores and modifiers for each ability score
        ability_scores_raw = self.base.ability_scores

        for a in self.race.asi.keys():
            ability_scores_raw[a] += self.race.asi[a]

        ability_scores_p = {}
        for a in ability_scores_raw.keys():
            score = ability_scores_raw[a]
            ability_scores_p[a] = {
                'score': score,
                'modifier': _modifier(score),
            }

        return ability_scores_p

    @property
    def armor_class(self):
        return (10 + _modifier(self.base._dex))

    @property
    def initiative(self):
        return (_modifier(self.base._dex))

    @property
    def max_hit_points(self):
        hit_points = 0
        for c in self.classes:
            if hit_points <= 0:
                hit_points = c.hit_die + _modifier(self.base._con)
            else:
                hit_points += math.ceil(c.hit_die/2) + _modifier(self.base._con)
        return hit_points
    
    @property
    def total_hit_dice(self):
        # A bit more complex because of multiclassing feature
        hit_dice = {}
        for c in self.classes:
            hit_die = 'd{}'.format(c.hit_die)
            if hit_die not in hit_dice:
                hit_dice[hit_die] = 1
            else:
                hit_dice[hit_die] += 1
        return hit_dice
    
    @property
    def saving_throws(self):
        saving_throws = self.classes[0].saving_throws
        saving_throws_p = {}
        ability_scores = self.ability_scores
        for a in ability_scores.keys():
            saving_throws_p[a] = ability_scores[a]['modifier']
            if a in saving_throws:
               saving_throws_p[a] += self.proficiency_bonus
        return saving_throws_p
    
    @property
    def skill_proficiencies(self):
        # TODO i think that each class should be responsible for
        # giving the PC class the skill proficiencies, as opposed
        # to the PC class trying to parse through everything
        # AKA do this to most of the rest of this class
        skill_proficiencies = (self.classes[0].skills + self.background.skills)
        ability_scores = self.ability_scores

        skill_proficiencies_p = {}
        for ability in SKILL_PROFICIENCIES.keys():
            for skill in SKILL_PROFICIENCIES[ability]:
                skill_proficiencies_p[skill] = {
                    'ability': ability,
                    'is_proficient': False,
                }
                skill_proficiencies_p[skill]['modifier'] = ability_scores[ability]['modifier']
                if skill in skill_proficiencies:
                    skill_proficiencies_p[skill]['is_proficient'] = True
                    skill_proficiencies_p[skill]['modifier'] += self.proficiency_bonus
        return skill_proficiencies_p
    
    @property
    def class_proficiencies(self):
      return self.classes[0].proficiencies
    
    @property
    def languages(self):
      return (self.race.languages + self.background.languages)

    def get_features(self):
        skill_features = {}
        for c in self.classes:
            skill_features = { **skill_features, **c.features }
        return skill_features
    
    def get_spellcasting(self):
        spellcasting_p = {}
        for c in self.classes:
            if c.spellcasting:
                spellcasting_p = c.spellcasting.__json__()
        return spellcasting_p

    def __json__(self):
        j_classes = []
        for c in self.classes:
            j_classes.append(c.__json__())
        j = self.base.__json__()
        j['classes'] = j_classes

        if self.race:
            j['race'] = self.race.__json__()
        
        if self.background:
            j['background'] = self.background.__json__()
    
        return j
    
    def generate_character_sheet(self):
        j = {
            'name': self.name,
            'basic': {
                'race': self.race_name,
                'class': self.class_name,
                'level': self.level,
                'background': self.background_name,
            },
            'proficiency_bonus': self.proficiency_bonus,
            'ability_scores': self.ability_scores,
            'saving_throws': self.saving_throws,
            'skills': self.skill_proficiencies,
            'combat': {
                'armor_class': self.armor_class,
                'initiative': self.initiative,
                'speed': self.speed,
            },
            'hit_points': {
                'max_hp': self.max_hit_points,
                'total_hit_dice': self.total_hit_dice,
            },
            'traits_and_features': {
                'size': self.size,
                # TODO when doing the traits, this can have some replication
                # this is in mind with the character sheet generator
                # and listing where things came from vs. actually deriving
                # the total calculations
                'racial_traits': self.race.traits,
                'languages': self.languages,
                'class_features': self.get_features(),
                'class_proficiencies': self.class_proficiencies,
                'background_feature': self.background.feature,
                'background_proficiencies': self.background.proficiencies,
            },
            'spellcasting': self.get_spellcasting(),
        }
        return j
