
import abc

from ddddd.entity.character import trait


class Vocation(object, metaclass=abc.ABCMeta):
    """
    A representation of a player character (PC) vocation.
    In 5e, this would be called a "class", but because Python has the word "class"
    as a keyword, this class is renamed to avoid confusion. In the presentation
    layer, a vocation would be called a "class"
    """
    def __init__(self, name, level, hit_die,
                 proficiencies, saving_throws, skill_proficiencies, features, asi,
                 spellcasting=None, feats=None):
        self.name = name
        self.level = level
        self.hit_die = hit_die
        self.proficiencies = proficiencies
        self.saving_throws = saving_throws
        self.skills = skill_proficiencies
        self._features = features
        self.asi = asi if asi else {}
        self.spellcasting = spellcasting
        self.feats = feats if feats else []

    def _append_feature(self, f_key, feature):
        self._features[f_key] = feature

    def _aggregate_asi_or_feat(self, kwargs, level):
        asi_key = 'ability_score_increase_{}'.format(level)
        feat_key = 'feat_{}'.format(level)
        if asi_key in kwargs:
            asi = kwargs[asi_key]
            for ability in asi.keys():
                if ability not in self.asi:
                    self.asi[ability] = asi[ability]
                else:
                    self.asi[ability] = self.asi[ability].combine(asi[ability])
        elif feat_key in kwargs:
            self.feats.append(kwargs[feat_key])

    @property
    def features(self):
        return list(self._features.values())
    
    @property
    def languages(self):
        lang = list(filter(lambda f: isinstance(f, trait.LanguagesKnown), self.features))
        agg_languages = trait.LanguagesKnown(languages=[])
        for l_feature in lang:
            agg_languages.languages = agg_languages.languages + l_feature.languages
        return agg_languages

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
            elif i == 6:
                self._add_level_6_features(**kwargs)
            elif i == 7:
                self._add_level_7_features(**kwargs)
            elif i == 8:
                self._add_level_8_features(**kwargs)
            elif i == 9:
                self._add_level_9_features(**kwargs)
            elif i == 10:
                self._add_level_10_features(**kwargs)
            elif i == 11:
                self._add_level_11_features(**kwargs)
            elif i == 12:
                self._add_level_12_features(**kwargs)
            elif i == 13:
                self._add_level_13_features(**kwargs)
            elif i == 14:
                self._add_level_14_features(**kwargs)
            elif i == 15:
                self._add_level_15_features(**kwargs)
            elif i == 16:
                self._add_level_16_features(**kwargs)
            elif i == 17:
                self._add_level_17_features(**kwargs)
            elif i == 18:
                self._add_level_18_features(**kwargs)
            elif i == 19:
                self._add_level_19_features(**kwargs)
            elif i == 20:
                self._add_level_20_features(**kwargs)
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

    @abc.abstractmethod
    def _add_level_6_features(self, **kwargs):
        return {}

    @abc.abstractmethod
    def _add_level_7_features(self, **kwargs):
        return {}

    @abc.abstractmethod
    def _add_level_8_features(self, **kwargs):
        return {}

    @abc.abstractmethod
    def _add_level_9_features(self, **kwargs):
        return {}

    @abc.abstractmethod
    def _add_level_10_features(self, **kwargs):
        return {}

    @abc.abstractmethod
    def _add_level_11_features(self, **kwargs):
        return {}

    @abc.abstractmethod
    def _add_level_12_features(self, **kwargs):
        return {}

    @abc.abstractmethod
    def _add_level_13_features(self, **kwargs):
        return {}

    @abc.abstractmethod
    def _add_level_14_features(self, **kwargs):
        return {}

    @abc.abstractmethod
    def _add_level_15_features(self, **kwargs):
        return {}

    @abc.abstractmethod
    def _add_level_16_features(self, **kwargs):
        return {}

    @abc.abstractmethod
    def _add_level_17_features(self, **kwargs):
        return {}

    @abc.abstractmethod
    def _add_level_18_features(self, **kwargs):
        return {}

    @abc.abstractmethod
    def _add_level_19_features(self, **kwargs):
        return {}

    @abc.abstractmethod
    def _add_level_20_features(self, **kwargs):
        return {}
