import math

from ddddd.entity.character.base import AbilityScore
from ddddd.entity.character import feature, base
from ddddd.entity.character.feature import Expertise
from ddddd.entity.character.vocation import Vocation
from ddddd.items import weapons


class Rogue(Vocation):
    def __init__(self, skill_proficiencies, expertise):
        def_features = {
            'sneak_attack': SneakAttack(level=1),
            'thieves_cant': feature.LanguagesKnown(name='Thieves'' Cant',
                                                   description='During your rogue Training you learned thieves'' cant, \
                                                 a Secret mix of dialect, jargon, and code that allows you to hide messages \
                                                 in seemingly normal conversation.',
                                                   languages=[base.Languages.THIEVES_CANT]),
            'expertise': expertise,
        }

        super(Rogue, self).__init__(name='Rogue',
                                    level=1,
                                    hit_die=8,
                                    proficiencies={
                                        base.ARMOR_PROFICIENCY: feature.ArmorProficiency(name='Armor Proficiency',
                                                                                         proficiencies=['light']),
                                        base.WEAPON_PROFICIENCY: feature.WeaponProficiency(name='Weapon Proficiency',
                                                                                           proficiencies=['simple',
                                                                                                        'hand crossbow',
                                                                                                        'longsword',
                                                                                                        'rapier',
                                                                                                        'shortsword']),
                                        base.TOOL_PROFICIENCY: feature.ToolProficiency(proficiencies=['thieves_tools'])
                                    },
                                    saving_throws=[AbilityScore.DEX, AbilityScore.INT],
                                    skill_proficiencies=skill_proficiencies,
                                    features=def_features,
                                    spellcasting=None,
                                    asi=None)

    def _add_level_2_features(self, **kwargs):
        self._append_feature('sneak_attack', feature=SneakAttack(level=self.level))
        self._append_feature('cunning_action',
                             feature=feature.Feature(name='Cunning Action',
                                                     description='Starting at 2nd level, your quick thinking and agility \
                                                 allow you to move and act quickly.'))

    def _add_level_3_features(self, **kwargs):
        self._append_feature('sneak_attack', feature=SneakAttack(level=self.level))
        new_gaming_set = kwargs['gaming_set']
        for proficiency in ['disguise_kit', 'forgery_kit', new_gaming_set]:
            self.proficiencies[base.TOOL_PROFICIENCY].proficiencies.append(proficiency)

        self._append_feature('master_of_intrigue',
                             feature=feature.Feature(name='Master of Intrigue',
                                                     description='You can unerringly mimic the speech patterns and accent of a creature \
                                                 that you hear speak for at least 1 minute.'))

        new_languages = kwargs[base.LANGUAGES]
        self._append_feature('master_of_intrigue_languages',
                             feature=feature.LanguagesKnown(name='Master of Intrigue: Languages',
                                                            languages=new_languages.languages))

        self._append_feature('master_of_tactics',
                             feature=feature.Feature(name='Master of Tactics',
                                                     description='Starting at 3rd level, you can use the Help action as a bonus action. \
                                                 Additionally, when you use the Help action to aid an ally in attacking a creature, \
                                                 the target of that attack can be within 30 feet of you, rather than 5 feet of you, \
                                                 if the target can see or hear you.'))

    def _add_level_4_features(self, **kwargs):
        self._append_feature('sneak_attack', feature=SneakAttack(level=self.level))

        self._aggregate_asi_or_feat(kwargs, level=4)

    def _add_level_5_features(self, **kwargs):
        self._append_feature('sneak_attack', feature=SneakAttack(level=self.level))

        self._append_feature('uncanny_dodge',
                             feature=feature.Feature(name='Uncanny Dodge',
                                                     description='Starting at 5th level, when an attacker that \
                                                 you can see hits you with an Attack, you can use your Reaction \
                                                 to halve the attack''s damage against you.'))

    def _add_level_6_features(self, **kwargs):
        self._append_feature('sneak_attack', feature=SneakAttack(level=self.level))
        old_expertise = self._features['expertise']
        new_expertise = kwargs['expertise_6']
        expert_skills = old_expertise.skills + new_expertise.skills
        expert_proficiencies = old_expertise.proficiencies + new_expertise.proficiencies
        self._append_feature('expertise', Expertise(skills=expert_skills, proficiencies=expert_proficiencies))

    def _add_level_7_features(self, **kwargs):
        self._append_feature('sneak_attack', feature=SneakAttack(level=self.level))

        self._append_feature('evasion',
                             feature=feature.Feature(name='Evasion',
                                                     description='Beginning at 7th level, you can nimbly dodge \
                                                     out of the way of certain area effects.'))

    def _add_level_8_features(self, **kwargs):
        self._append_feature('sneak_attack', feature=SneakAttack(level=self.level))

        self._aggregate_asi_or_feat(kwargs, level=8)

    def _add_level_9_features(self, **kwargs):
        self._append_feature('sneak_attack', feature=SneakAttack(level=self.level))

        self._append_feature('insightful_manipulator',
                             feature=feature.Feature(name='Insightful Manipulator',
                                                     description='You can learn certain information about \
                                                     its capabilities compared to your own'))

    def _add_level_10_features(self, **kwargs):
        self._append_feature('sneak_attack', feature=SneakAttack(level=self.level))

        self._aggregate_asi_or_feat(kwargs, level=10)

    def _add_level_11_features(self, **kwargs):
        self._append_feature('sneak_attack', feature=SneakAttack(level=self.level))

        self._append_feature('reliable_talent',
                             feature=feature.Feature(name='Reliable Talent',
                                                     description='By 11th level, you have refined your chosen skills \
                                                     until they approach perfection.'))

    def _add_level_12_features(self, **kwargs):
        self._append_feature('sneak_attack', feature=SneakAttack(level=self.level))

        self._aggregate_asi_or_feat(kwargs, level=12)

    def _add_level_13_features(self, **kwargs):
        self._append_feature('sneak_attack', feature=SneakAttack(level=self.level))

        self._append_feature('misdirection',
                             feature=feature.Feature(name='Misdirection',
                                                     description='Beginning at 13th level, you can sometimes cause \
                                                     another creature to suffer an attack meant for you.'))

    def _add_level_14_features(self, **kwargs):
        self._append_feature('sneak_attack', feature=SneakAttack(level=self.level))

        self._append_feature('blindsense',
                             feature=feature.Feature(name='Blindsense',
                                                     description='Starting at 14th level, if you are able to hear, \
                                                     you are aware of the location of any hidden or invisible creature \
                                                     within 10 feet of you.'))

    def _add_level_15_features(self, **kwargs):
        self._append_feature('sneak_attack', feature=SneakAttack(level=self.level))

        self._append_feature('slippery_mind',
                             feature=feature.Feature(name='Slippery Mind',
                                                     description='By 15th level, you have acquired greater \
                                                     mental strength. You gain proficiency in Wisdom saving throws.'))

    def _add_level_16_features(self, **kwargs):
        self._append_feature('sneak_attack', feature=SneakAttack(level=self.level))

        self._aggregate_asi_or_feat(kwargs, level=16)

    def _add_level_17_features(self, **kwargs):
        self._append_feature('sneak_attack', feature=SneakAttack(level=self.level))

        self._append_feature('soul_of_deceit',
                             feature=feature.Feature(name='Soul of Deceit',
                                                     description='Starting at 17th level, your thoughts can''t be read \
                                                     by telepathy or other means, unless you allow it.'))

    def _add_level_18_features(self, **kwargs):
        self._append_feature('sneak_attack', feature=SneakAttack(level=self.level))

        self._append_feature('elusive',
                             feature=feature.Feature(name='Elusive',
                                                     description='Beginning at 18th level, you are so evasive \
                                                     that attackers rarely gain the upper hand against you.'))

    def _add_level_19_features(self, **kwargs):
        self._append_feature('sneak_attack', feature=SneakAttack(level=self.level))

        self._aggregate_asi_or_feat(kwargs, level=19)

    def _add_level_20_features(self, **kwargs):
        self._append_feature('sneak_attack', feature=SneakAttack(level=self.level))

        self._append_feature('stroke_of_luck',
                             feature=feature.Feature(name='Stroke of Luck',
                                                     description='At 20th level, you have an uncanny knack \
                                                     for succeeding when you need to.'))


class SneakAttack(feature.EnhanceDamage):
    def __init__(self, level):
        attack_bonus = '{}d6'.format(math.floor((level+1)/2))
        super(SneakAttack, self).__init__(name='Sneak Attack',
                                          description='Beginning at 1st level, you know how to strike subtly \
                                          and exploit a foe''s distraction. \
                                          Sneak attack bonus = {}'.format(attack_bonus),
                                          attack_bonus=attack_bonus)

    def qualifies(self, weapon):
        if not isinstance(weapon, weapons.Weapon):  # Must be a weapon
            return False
        for prop in [weapons.FINESSE, weapons.AMMUNITION, weapons.THROWN]:
            if prop in weapon.properties:  # Must be a finesse or ranged weapon
                return True
        return False
