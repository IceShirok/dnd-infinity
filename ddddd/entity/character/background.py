
from ddddd.entity import base
from ddddd.entity.base import Skills
from ddddd.entity.character import trait


class PlayerBackground(object):
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
        self.languages = languages

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


#############################
# Custom backgrounds
#############################

class Criminal(PlayerBackground):
    def __init__(self):
        feature = trait.Trait(name='Criminal Contact',
                              description='You have a reliable and trustworthy contact who acts as \
                              your liaison to a network of other criminals. ...')
        proficiencies = {
            base.SKILLS: [Skills.DECEPTION, Skills.STEALTH],
            base.TOOL_PROFICIENCY: trait.ToolProficiency(name='Tool Proficiency',
                                                         proficiencies=['thieves_tools', 'bone_dice']),
        }
        super(Criminal, self).__init__(name='Criminal',
                                       feature=feature,
                                       proficiencies=proficiencies,
                                       languages=None)


class Noble(PlayerBackground):
    def __init__(self, tool_proficiency, languages):
        feature = trait.Trait(name='Position of Privilege',
                              description='Thanks to your noble birth, people are inclined to think the best of you.')
        proficiencies = {
            base.SKILLS: [Skills.PERSUASION, Skills.HISTORY],
            base.TOOL_PROFICIENCY: tool_proficiency,
        }
        super(Noble, self).__init__(name='Noble',
                                    feature=feature,
                                    proficiencies=proficiencies,
                                    languages=languages)


class Sage(PlayerBackground):
    def __init__(self, languages):
        feature = trait.Trait(name='Researcher',
                              description='When you attempt to learn or recall a piece of lore, if you do not know \
                              that information, you often know where and from whom you can obtain it ...')
        proficiencies = {
            base.SKILLS: [Skills.ARCANA, Skills.HISTORY],
        }
        super(Sage, self).__init__(name='Sage',
                                   feature=feature,
                                   proficiencies=proficiencies,
                                   languages=languages)
