from ddddd.entity.character.base import Skills
from ddddd.entity.character import race, background, pc, spells, base
from ddddd.entity.character.vocations import ranger, cleric, rogue
from ddddd.entity.character import feature
from ddddd.items import items, armor, weapons

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def get_available_characters():
    return {
        'dorian': {
            'max_level': 5,
            'create': create_dorian,
        },
        'tamiphi': {
            'max_level': 20,
            'create': create_tamiphi,
        },
        'fethri': {
            'max_level': 5,
            'create': create_fethri,
        },
    }


def create_dorian(level=5):
    """
    Creates Dorian, a dwarf ranger.
    The dwarf race provides a suite of features while also giving choices
    to proficiencies and stat-altering features.
    The ranger class provides a good mix of features that a PC can have,
    as a martial class with basic spellcasting abilities.
    :param level: the character level
    :return: Dorian the dwarf ranger
    """
    base_ = base.EntityBase("Dorian Sapbleden", 16, 10, 14, 12, 14, 8, level=level)
    tool_prof = [
        feature.ToolProficiency(name='Tool Proficiency',
                                proficiencies=['brewers_kit'])
    ]
    race_ = race.HillDwarf(traits=tool_prof)
    vocation = ranger.Ranger(skill_proficiencies=[Skills.ATHLETICS, Skills.ANIMAL_HANDLING, Skills.SURVIVAL],
                             favored_enemy='plants',
                             languages='elvish',
                             favored_terrain='forest')
    if level > 1:
        vocation.level_to(level=level,
                          fighting_style='two_weapon_fighting',
                          archetype_feature='colossus_slayer',
                          ability_score_increase_4={
                              base.AbilityScore.STR: base.AbilityScoreIncrease(base.AbilityScore.STR, 2),
                          })
    bg = background.Criminal()

    worn_items = items.WornItems()
    worn_items.don_armor(armor.CHAIN_MAIL)
    worn_items.equip_weapon(weapons.HANDAXE)
    worn_items.equip_weapon(weapons.HANDAXE)
    worn_items.equip_weapon(weapons.LONGBOW)

    backpack = items.generate_burglars_pack()
    backpack.add_item(armor.CHAIN_SHIRT)
    backpack.add_item(armor.LEATHER_ARMOR)

    dorian = pc.PlayerCharacter(base_, race_, vocation, bg, worn_items, backpack)
    return dorian


def create_tamiphi(level=1):
    """
    Creates Tamiphi, a gnome cleric.
    The gnome race is extremely straightforward, as it provides all
    features without user input.
    The cleric class, especially a knowledge domain cleric, is a pure
    spellcaster that is suited to test out the spellcasting feature.
    :param level: the character level
    :return: Tamiphi the gnome cleric
    """
    base_ = base.EntityBase("Tamiphi Tockentell", 10, 12, 15, 14, 18, 7, level=level)
    race_ = race.RockGnome()
    class_languages = feature.LanguagesKnown(languages=[base.Languages.DRACONIC, base.Languages.DWARVISH])
    class_skills = [Skills.ARCANA, Skills.HISTORY]
    class_cantrips = [spells.SACRED_FLAME, spells.GUIDANCE, spells.SPARE_THE_DYING]
    vocation = cleric.Cleric(skill_proficiencies=[Skills.INSIGHT, Skills.RELIGION, Skills.ARCANA, Skills.PERSUASION],
                             cleric_domain='knowledge', cantrips=class_cantrips,
                             languages=class_languages, skills=class_skills)
    if level > 1:
        vocation.level_to(level=level,
                          cantrip_4=spells.WORD_OF_RADIANCE,
                          ability_score_increase_4={
                              base.AbilityScore.WIS: base.AbilityScoreIncrease(base.AbilityScore.WIS, 2),
                          },
                          feat_8=feature.WarCaster(),
                          cantrip_10=spells.MENDING,
                          ability_score_increase_12={
                              base.AbilityScore.INT: base.AbilityScoreIncrease(base.AbilityScore.INT, 2),
                          },
                          ability_score_increase_16={
                              base.AbilityScore.INT: base.AbilityScoreIncrease(base.AbilityScore.INT, 2),
                          },
                          ability_score_increase_19={
                              base.AbilityScore.CON: base.AbilityScoreIncrease(base.AbilityScore.CON, 2),
                          })
    bg_languages = feature.LanguagesKnown(languages=[base.Languages.CELESTIAL, base.Languages.INFERNAL])
    background_ = background.Sage(bg_languages)

    worn_items = items.WornItems()
    worn_items.equip_weapon(weapons.MACE)
    worn_items.don_armor(armor.CHAIN_SHIRT)

    backpack = items.generate_explorers_pack()
    tamiphi = pc.PlayerCharacter(base_, race_, vocation, background_, worn_items, backpack)
    return tamiphi


def create_fethri(level=1):
    """
    Creates Fethri, a tiefling rogue.
    The tiefling race is straightforward, providing a suite of features
    without user input.
    The rogue class, especially the mastermind, is perfect to test out
    aggregations of skills and attack features without needing to focus
    on spellcasting at all.
    :param level: the character level
    :return: Fethri the tiefling rogue
    """
    base_ = base.EntityBase("Fethri Winterwhisper", 10, 14, 12, 15, 11, 12, level=level)
    race_ = race.Tiefling()
    vocation = rogue.Rogue(skill_proficiencies=[Skills.INVESTIGATION,
                                                Skills.DECEPTION,
                                                Skills.STEALTH],
                           expertise=feature.Expertise(skills=[Skills.INVESTIGATION,
                                                               Skills.DECEPTION],
                                                       proficiencies=None)
                           )
    if level > 1:
        vocation.level_to(level=level,
                          roguish_archetype='mastermind',
                          gaming_set='bone_dice',
                          languages=feature.LanguagesKnown(languages=[base.Languages.UNDERCOMMON,
                                                                      base.Languages.ELVISH]),
                          ability_score_increase_4={
                              base.AbilityScore.DEX: base.AbilityScoreIncrease(base.AbilityScore.DEX, 2),
                          },
                          expertise_6=feature.Expertise(skills=[Skills.STEALTH],
                                                        proficiencies=['thieves_tools']),
                          ability_score_increase_8={
                              base.AbilityScore.DEX: base.AbilityScoreIncrease(base.AbilityScore.DEX, 2),
                          },
                          ability_score_increase_10={
                              base.AbilityScore.INT: base.AbilityScoreIncrease(base.AbilityScore.INT, 2),
                          },
                          ability_score_increase_12={
                              base.AbilityScore.DEX: base.AbilityScoreIncrease(base.AbilityScore.DEX, 2),
                          },
                          ability_score_increase_16={
                              base.AbilityScore.CHA: base.AbilityScoreIncrease(base.AbilityScore.CHA, 2),
                          },
                          ability_score_increase_19={
                              base.AbilityScore.INT: base.AbilityScoreIncrease(base.AbilityScore.INT, 2),
                          }
        )

    background_ = background.Noble(tool_proficiency=feature.ToolProficiency(proficiencies=['chess_set']),
                                   languages=feature.LanguagesKnown(languages=[base.Languages.DRACONIC]))

    worn_items = items.WornItems()
    worn_items.don_armor(armor.LEATHER_ARMOR)
    worn_items.equip_weapon(weapons.RAPIER)
    worn_items.equip_weapon(weapons.SHORTBOW)

    backpack = items.generate_burglars_pack()
    fethri = pc.PlayerCharacter(base_, race_, vocation, background_, worn_items, backpack)
    return fethri
