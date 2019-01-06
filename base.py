
import json
import math

class Jsonable(object):
    def __json__(self):
        pass

    def __str__(self):
        return json.dumps(self.__json__(), indent=4, sort_keys=False)


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
        return math.floor((self.level + 3) / 4) + 1

