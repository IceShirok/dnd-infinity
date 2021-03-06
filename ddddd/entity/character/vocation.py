
from ddddd.entity.character import feature


class Vocation(object):
    """
    A representation of a player character (PC) vocation.
    In 5e, this would be called a "class", but because Python has the word "class"
    as a keyword, this class is renamed to avoid confusion. In the presentation
    layer, a vocation would be called a "class"
    """
    def __init__(self, name, level, hit_die,
                 proficiencies, saving_throws, skill_proficiencies, features,
                 asi=None, spellcasting=None, feats=None):
        self.name = name
        self.level = level
        self.hit_die = hit_die
        self.proficiencies = proficiencies
        self.saving_throws = saving_throws
        self.skills = skill_proficiencies
        self._features = features if features else {}
        self.asi = asi if asi else {}
        self.spellcasting = spellcasting
        self.feats = feats if feats else []
        self.specialization = None

    def _add_level_based_features(self, level):
        """
        This function is called after every level.
        Each specific vocation may or may not need to override this.
        """
        pass

    def _add_specialization_features(self, level, **kwargs):
        add_level_features = getattr(self.specialization, 'add_level_{}_features'.format(level), None)
        if self.specialization and add_level_features:
            new_stuff = add_level_features(**kwargs)
            if 'features' in new_stuff:
                for key, f in new_stuff['features'].items():
                    self._append_feature(key, f)
            if 'proficiencies' in new_stuff:
                for key, p in new_stuff['proficiencies'].items():
                    self.proficiencies[key].proficiencies.extend(p)

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
        lang = list(filter(lambda f: isinstance(f, feature.LanguagesKnown), self.features))
        agg_languages = feature.LanguagesKnown(languages=[])
        for l_feature in lang:
            agg_languages.languages = agg_languages.languages + l_feature.languages
        return agg_languages

    def level_to(self, level, **kwargs):
        if level <= self.level:
            raise ValueError('This class is already larger than requested!')

        start, end = (self.level+1, level+1)
        for i in range(start, end):
            self.level = i
            if 1 < level <= 20:
                # LOL Python has amazing reflection skills, yay intepreted languages
                getattr(self, '_add_level_{}_features'.format(i))(**kwargs)
            else:
                raise ValueError('Invalid level!')

    def _add_level_1_features(self, **kwargs):
        self._add_level_based_features(1)
        self._add_specialization_features(1, **kwargs)

    def _add_level_2_features(self, **kwargs):
        self._add_level_based_features(2)
        self._add_specialization_features(2, **kwargs)

    def _add_level_3_features(self, **kwargs):
        self._add_level_based_features(3)
        self._add_specialization_features(3, **kwargs)

    def _add_level_4_features(self, **kwargs):
        self._add_level_based_features(4)
        self._add_specialization_features(4, **kwargs)

    def _add_level_5_features(self, **kwargs):
        self._add_level_based_features(5)
        self._add_specialization_features(5, **kwargs)

    def _add_level_6_features(self, **kwargs):
        self._add_level_based_features(6)
        self._add_specialization_features(6, **kwargs)

    def _add_level_7_features(self, **kwargs):
        self._add_level_based_features(7)
        self._add_specialization_features(7, **kwargs)

    def _add_level_8_features(self, **kwargs):
        self._add_level_based_features(8)
        self._add_specialization_features(8, **kwargs)

    def _add_level_9_features(self, **kwargs):
        self._add_level_based_features(9)
        self._add_specialization_features(9, **kwargs)

    def _add_level_10_features(self, **kwargs):
        self._add_level_based_features(10)
        self._add_specialization_features(10, **kwargs)

    def _add_level_11_features(self, **kwargs):
        self._add_level_based_features(11)
        self._add_specialization_features(11, **kwargs)

    def _add_level_12_features(self, **kwargs):
        self._add_level_based_features(12)
        self._add_specialization_features(12, **kwargs)

    def _add_level_13_features(self, **kwargs):
        self._add_level_based_features(13)
        self._add_specialization_features(13, **kwargs)

    def _add_level_14_features(self, **kwargs):
        self._add_level_based_features(14)
        self._add_specialization_features(14, **kwargs)

    def _add_level_15_features(self, **kwargs):
        self._add_level_based_features(15)
        self._add_specialization_features(15, **kwargs)

    def _add_level_16_features(self, **kwargs):
        self._add_level_based_features(16)
        self._add_specialization_features(16, **kwargs)

    def _add_level_17_features(self, **kwargs):
        self._add_level_based_features(17)
        self._add_specialization_features(17, **kwargs)

    def _add_level_18_features(self, **kwargs):
        self._add_level_based_features(18)
        self._add_specialization_features(18, **kwargs)

    def _add_level_19_features(self, **kwargs):
        self._add_level_based_features(19)
        self._add_specialization_features(19, **kwargs)

    def _add_level_20_features(self, **kwargs):
        self._add_level_based_features(20)
        self._add_specialization_features(20, **kwargs)
