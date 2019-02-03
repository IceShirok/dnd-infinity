
import abc

from ddddd.entity import base
from ddddd.entity.character import trait


class PlayerClass(object, metaclass=abc.ABCMeta):
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
        self.asi = asi if asi else {}
        self.spellcasting = spellcasting
    
    @property
    def languages(self):
        lang = list(filter(lambda f: isinstance(f, trait.LanguagesKnown), self.features))
        if len(lang) > 0:
            return lang[0]
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
