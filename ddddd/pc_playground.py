from ddddd.entity import base
from ddddd.entity.base import Skills
from ddddd.entity.character import race, background, pc, equipment, spells
from ddddd.entity.character.vocation import ranger, cleric, rogue
from ddddd.entity.character import trait

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


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
    base_ = pc.PlayerBase("Dorian Sapbleden", 16, 10, 14, 12, 14, 8, level=level)
    tool_prof = [
        trait.ToolProficiency(name='Tool Proficiency',
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
                          ability_score_increase={
                              base.AbilityScore.STR: base.AbilityScoreIncrease(base.AbilityScore.STR, 2),
                          })
    bg = background.Criminal()

    def generate_equipment():
        logger.debug('Displaying worn items')
        worn_items = equipment.WornItems()

        rondel = equipment.Weapon('handaxe', category='simple', damage='1d6 slashing', price=5, weight=2,
                                  properties=['light', 'thrown (range 20/60)'])
        lefon = equipment.Weapon('handaxe', category='simple', damage='1d6 slashing', price=5, weight=2,
                                 properties=['light', 'thrown (range 20/60)'])
        longbow = equipment.Weapon('longbow', category='martial', damage='1d8 piercing', price=50, weight=2,
                                   properties=['ammunition (range 150/600)', 'heavy', 'two-handed'])
        worn_items.don_armor(equipment.CHAIN_MAIL)
        worn_items.equip_weapon(rondel)
        worn_items.equip_weapon(lefon)
        worn_items.equip_weapon(longbow)
        return worn_items

    equip = generate_equipment()

    backpack = generate_burglars_pack()
    backpack.add_item(equipment.CHAIN_SHIRT)
    backpack.add_item(equipment.LEATHER_ARMOR)

    dorian = pc.PlayerCharacter(base_, race_, vocation, bg, equip, backpack)
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
    base_ = pc.PlayerBase("Tamiphi Tockentell", 10, 11, 15, 14, 16, 7, level=level)
    race_ = race.RockGnome()
    class_languages = trait.LanguagesKnown(languages=[base.Languages.DRACONIC, base.Languages.DWARVISH])
    class_cantrips = [spells.SACRED_FLAME, spells.GUIDANCE, spells.SPARE_THE_DYING]
    vocation = cleric.Cleric(skill_proficiencies=[Skills.INSIGHT, Skills.RELIGION, Skills.ARCANA, Skills.PERSUASION],
                             languages=class_languages, cantrips=class_cantrips)
    if level > 1:
        vocation.level_to(level=level,
                          cantrip_4=spells.WORD_OF_RADIANCE,
                          ability_score_increase={
                              base.AbilityScore.WIS: base.AbilityScoreIncrease(base.AbilityScore.WIS, 2),
                          })
    bg_languages = trait.LanguagesKnown(languages=[base.Languages.CELESTIAL, base.Languages.INFERNAL])
    background_ = background.Sage(bg_languages)

    def generate_equipment():
        worn_items = equipment.WornItems()
        mace = equipment.Weapon('Mace', category='simple', damage='1d6 bludgeoning', price=5, weight=4,
                                properties=[])
        worn_items.equip_weapon(mace)

        def calc_medium_armor_rating(dex_mod):
            # chain shirt
            return 13 + min(dex_mod, 2)

        worn_items.don_armor(equipment.Armor('Chain Shirt', price=50, weight=20,
                                             armor_class=calc_medium_armor_rating, strength=0, stealth=''))
        return worn_items

    equip = generate_equipment()
    backpack = generate_burglars_pack()
    tamiphi = pc.PlayerCharacter(base_, race_, vocation, background_, equip, backpack)
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
    base_ = pc.PlayerBase("Fethri Winterwhisper", 10, 14, 12, 15, 11, 12, level=level)
    race_ = race.Tiefling()
    vocation = rogue.Rogue(skill_proficiencies=[Skills.INVESTIGATION,
                                                Skills.DECEPTION,
                                                Skills.STEALTH],
                           expertise=trait.Expertise(skills=[Skills.INVESTIGATION,
                                                             Skills.DECEPTION],
                                                     proficiencies=None)
                           )
    if level > 1:
        vocation.level_to(level=level,
                          gaming_set='bone_dice',
                          languages=trait.LanguagesKnown(languages=[base.Languages.CELESTIAL,
                                                                    base.Languages.DWARVISH]),
                          ability_score_increase={
                              base.AbilityScore.INT: base.AbilityScoreIncrease(base.AbilityScore.INT, 2),
                          })
    background_ = background.Noble(tool_proficiency=trait.ToolProficiency(proficiencies=['chess_set']),
                                   languages=trait.LanguagesKnown(languages=[base.Languages.DRACONIC]))

    def generate_equipment():
        logger.debug('Displaying worn items')
        worn_items = equipment.WornItems()

        def calc_light_armor_rating(dex_mod):
            # leather armor
            return 11 + dex_mod

        armor = equipment.Armor('Leather Armor', price=10, weight=10, armor_class=calc_light_armor_rating,
                                strength=0, stealth='')
        longbow = equipment.Weapon('rapier', category='martial', damage='1d8 piercing', price=25, weight=2,
                                   properties=['finesse'])
        worn_items.don_armor(armor)
        worn_items.equip_weapon(longbow)
        return worn_items

    equip = generate_equipment()
    backpack = generate_burglars_pack()
    fethri = pc.PlayerCharacter(base_, race_, vocation, background_, equip, backpack)
    return fethri


def generate_burglars_pack():
    backpack = equipment.Backpack(copper_pieces=0, silver_pieces=0, gold_pieces=15, platnium_pieces=0, items=None)
    backpack.add_item(equipment.Item('Ball Bearings', price=1, weight=2))
    backpack.add_item(equipment.Item('String', price=0, weight=0, description='10 ft of string'))
    backpack.add_item(equipment.Item('Bell', price=1, weight=0))
    backpack.add_item(equipment.Item('Candle', price=0, weight=0, quantity=5))
    backpack.add_item(equipment.Item('Crowbar', price=2, weight=5, quantity=2))
    backpack.add_item(equipment.Item('Hammer', price=1, weight=3))
    backpack.add_item(equipment.Item('Piton', price=0, weight=1, quantity=10))
    backpack.add_item(equipment.Item('Hooded Lantern', price=4, weight=2))
    backpack.add_item(equipment.Item('Flask of Oil', price=1, weight=1, quantity=2))
    backpack.add_item(equipment.Item('Rations', price=0.5, weight=2, quantity=5))
    backpack.add_item(equipment.Item('Tinderbox', price=1, weight=1))
    backpack.add_item(equipment.Item('Waterskin', price=1, weight=5))
    backpack.add_item(equipment.Item('Hempen Rope', price=1, weight=10, description='50 ft of rope'))
    return backpack
