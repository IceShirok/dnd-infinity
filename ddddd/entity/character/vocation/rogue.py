from ddddd.entity import base
from ddddd.entity.base import AbilityScore, Skills, Languages, SpellTypes
from ddddd.entity.character import spells, trait
from ddddd.entity.character.cclass import PlayerClass


#############################
# Rogue
#############################

class Rogue(PlayerClass):
    def __init__(self, skill_proficiencies):
        def_features = [
            trait.Trait(name='Expertise',
                        description='At 1st level, choose two of your skill proficiencies, \
                        or one of your skill proficiencies and your proficiency with Thieves'' Tools. \
                        Your Proficiency Bonus is doubled for any ability check you make that uses \
                        either of the chosen proficiencies.'),
            trait.Trait(name='Sneak Attack',
                        description='Beginning at 1st level, you know how to strike subtly \
                        and exploit a foe''s distraction.'),
            trait.LanguagesKnown(name='Thieves'' Cant',
                                 description='During your rogue Training you learned thieves'' cant, \
                                 a Secret mix of dialect, jargon, and code that allows you to hide messages \
                                 in seemingly normal conversation.',
                                 languages=[base.Languages.THIEVES_CANT])
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
        pass

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
        pass
