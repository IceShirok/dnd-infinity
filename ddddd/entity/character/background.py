
from ddddd.entity import base
from ddddd.entity.base import Skills
from ddddd.entity.character import feature


class Background(object):
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

class Criminal(Background):
    def __init__(self):
        f = feature.Feature(name='Criminal Contact',
                            description='You have a reliable and trustworthy contact who acts as \
                            your liaison to a network of other criminals. ...')
        proficiencies = {
            base.SKILLS: [Skills.DECEPTION, Skills.STEALTH],
            base.TOOL_PROFICIENCY: feature.ToolProficiency(name='Tool Proficiency',
                                                           proficiencies=['thieves_tools', 'bone_dice']),
        }
        super(Criminal, self).__init__(name='Criminal',
                                       feature=f,
                                       proficiencies=proficiencies,
                                       languages=None)


class Noble(Background):
    def __init__(self, tool_proficiency, languages):
        f = feature.Feature(name='Position of Privilege',
                            description='Thanks to your noble birth, people are inclined to think the best of you.')
        proficiencies = {
            base.SKILLS: [Skills.PERSUASION, Skills.HISTORY],
            base.TOOL_PROFICIENCY: tool_proficiency,
        }
        super(Noble, self).__init__(name='Noble',
                                    feature=f,
                                    proficiencies=proficiencies,
                                    languages=languages)


class Sage(Background):
    def __init__(self, languages):
        f = feature.Feature(name='Researcher',
                            description='When you attempt to learn or recall a piece of lore, if you do not know \
                            that information, you often know where and from whom you can obtain it ...')
        proficiencies = {
            base.SKILLS: [Skills.ARCANA, Skills.HISTORY],
        }
        super(Sage, self).__init__(name='Sage',
                                   feature=f,
                                   proficiencies=proficiencies,
                                   languages=languages)
