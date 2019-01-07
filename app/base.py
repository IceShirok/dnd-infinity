
import json
import math

"""
An interface to allow objects to be viewed in a JSON format.
This is more for testing and debugging purposes, and some
features may be replaced with objects instead.
"""
class Jsonable(object):
    def __json__(self):
        pass

    def __str__(self):
        return json.dumps(self.__json__(), indent=4, sort_keys=False)


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

