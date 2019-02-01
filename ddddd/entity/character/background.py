
from ddddd.entity import base
from ddddd.entity.base import Skills
from ddddd.entity.character import trait


class PlayerBackground(base.Jsonable):
    """
    A player character's (PC) background.
    This doesn't change after a PC is created, but this is created
    separately because it is a separate section in the PHB and is
    easy to model as such.
    """

    def __init__(self, name, feature, proficiencies, languages):
        self.name = name
        self.feature = feature
        self.__proficiencies = proficiencies if proficiencies else {}
        self.languages = languages if languages else []

    def __json__(self):
        j = {
            base.BACKGROUND: self.name,
            base.FEATURES: self.feature,
            base.PROFICIENCIES: self.__proficiencies,
            base.LANGUAGES: self.languages,
        }
        return j

    @property
    def skills(self):
        if base.SKILLS in self.__proficiencies:
            return self.__proficiencies[base.SKILLS]
        return []

    @property
    def background_proficiencies(self):
        p = {**self.__proficiencies}
        return p

    @property
    def proficiencies(self):
        p = {**self.background_proficiencies}
        if base.SKILLS in p:
            p.pop(base.SKILLS)
        return p


class Criminal(PlayerBackground):
    def __init__(self):
        feature = trait.Trait(name='Criminal Contact',
                              description='You have a reliable and trustworthy contact who acts as \
                              your liaison to a network of other criminals. ...')
        proficiencies = {
            base.SKILLS: [Skills.DECEPTION, Skills.STEALTH],
            base.TOOLS: ['thieves_tools', 'bone_dice'],
        }
        super(Criminal, self).__init__(name='criminal',
                                       feature=feature,
                                       proficiencies=proficiencies,
                                       languages=[])
