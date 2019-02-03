from ddddd.entity import base
from ddddd.entity.base import AbilityScore, Skills, Languages, SpellTypes
from ddddd.entity.character import spells, trait
from ddddd.entity.character.cclass import Vocation


class Rogue(Vocation):
    def __init__(self, skill_proficiencies, expertise):
        def_features = [
            trait.Trait(name='Sneak Attack',
                        description='Beginning at 1st level, you know how to strike subtly \
                        and exploit a foe''s distraction.'),
            trait.LanguagesKnown(name='Thieves'' Cant',
                                 description='During your rogue Training you learned thieves'' cant, \
                                 a Secret mix of dialect, jargon, and code that allows you to hide messages \
                                 in seemingly normal conversation.',
                                 languages=[base.Languages.THIEVES_CANT]),
            expertise,
        ]

        super(Rogue, self).__init__(name='Rogue',
                                    level=1,
                                    hit_die=8,
                                    proficiencies={
                                        base.ARMOR_PROFICIENCY: trait.ArmorProficiency(name='Armor Proficiency',
                                                                                       proficiencies=['light']),
                                        base.WEAPON_PROFICIENCY: trait.WeaponProficiency(name='Weapon Proficiency',
                                                                                         proficiencies=['simple',
                                                                                                        'hand crossbow',
                                                                                                        'longsword',
                                                                                                        'rapier',
                                                                                                        'shortsword']),
                                        base.TOOL_PROFICIENCY: trait.ToolProficiency(proficiencies=['thieves_tools'])
                                    },
                                    saving_throws=[AbilityScore.DEX, AbilityScore.INT],
                                    skill_proficiencies=skill_proficiencies,
                                    features=def_features,
                                    spellcasting=None,
                                    asi=None)

    def _level_1_requirements(self):
        pass

    def _level_2_requirements(self):
        pass

    def _add_level_2_features(self, **kwargs):
        self.features.append(
            trait.Trait(name='Cunning Action',
                        description='Starting at 2nd level, your quick thinking and agility \
                        allow you to move and act quickly.')
        )

    def _level_3_requirements(self):
        pass

    def _add_level_3_features(self, **kwargs):
        new_gaming_set = kwargs['gaming_set']
        for proficiency in ['disguise_kit', 'forgery_kit', new_gaming_set]:
            self.proficiencies[base.TOOL_PROFICIENCY].proficiencies.append(proficiency)

        new_languages = kwargs[base.LANGUAGES]
        self.features.append(new_languages)

        self.features.append(
            trait.Trait(name='Master of Intrigue',
                        description='You can unerringly mimic the speech patterns and accent of a creature \
                        that you hear speak for at least 1 minute.')
        )

        self.features.append(
            trait.Trait(name='Master of Tactics',
                        description='Starting at 3rd level, you can use the Help action as a bonus action. \
                        Additionally, when you use the Help action to aid an ally in attacking a creature, \
                        the target of that attack can be within 30 feet of you, rather than 5 feet of you, \
                        if the target can see or hear you.')
        )

    def _level_4_requirements(self):
        pass

    def _add_level_4_features(self, **kwargs):
        ability_score_increase = kwargs['ability_score_increase']
        for ability in ability_score_increase.keys():
            if ability not in self.asi:
                self.asi[ability] = ability_score_increase[ability]
            else:
                self.asi[ability] = self.asi[ability].combine(ability_score_increase[ability])

    def _level_5_requirements(self):
        pass

    def _add_level_5_features(self, **kwargs):
        self.features.append(
            trait.Trait(name='Uncanny Dodge',
                        description='Starting at 5th level, when an attacker that you can see hits you with an Attack, \
                        you can use your Reaction to halve the attack''s damage against you.')
        )
