
from ddddd.entity import base
from ddddd.entity.base import Skills
from ddddd.entity.character import race, background, pc, equipment
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
    dorian_base = pc.PlayerBase("Dorian Sapbleden", 16, 10, 14, 12, 14, 8, level=level)
    tool_prof = [
        trait.ToolProficiency(name='Tool Proficiency',
                              proficiencies=['brewers_kit'])
    ]
    dorian_race = race.HillDwarf(traits=tool_prof)
    dorian_class = ranger.Ranger(skill_proficiencies=[Skills.ATHLETICS, Skills.ANIMAL_HANDLING, Skills.SURVIVAL],
                                 favored_enemy='plants',
                                 languages='elvish',
                                 favored_terrain='forest')
    if level > 1:
        dorian_class.level_to(level=level,
                              fighting_style='two_weapon_fighting',
                              archetype_feature='colossus_slayer',
                              ability_score_increase={
                                  base.AbilityScore.STR: base.AbilityScoreIncrease(base.AbilityScore.STR, 2),
                              })
    dorian_background = background.Criminal()

    def generate_backpack():
        logger.debug('Displaying equipment in backpack')
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

        def calc_light_armor_rating(dex_mod):
            # leather armor
            return 11 + dex_mod

        backpack.add_item(
            equipment.Armor('Leather Armor', price=10, weight=10, armor_class=calc_light_armor_rating, strength=0,
                            stealth=''))

        def calc_medium_armor_rating(dex_mod):
            # chain shirt
            return 13 + min(dex_mod, 2)

        backpack.add_item(
            equipment.Armor('Chain Shirt', price=50, weight=20, armor_class=calc_medium_armor_rating, strength=0,
                            stealth=''))

        return backpack

    def generate_equipment():
        logger.debug('Displaying worn items')
        worn_items = equipment.WornItems()

        def calc_heavy_armor_rating():
            # chain mail
            return 16

        armor = equipment.Armor('Chain Mail', price=75, weight=55, armor_class=calc_heavy_armor_rating, strength=15,
                                stealth='disadvantage')
        rondel = equipment.Weapon('handaxe', category='simple', damage='1d6 slashing', price=5, weight=2,
                                  properties=['light', 'thrown (range 20/60)'])
        lefon = equipment.Weapon('handaxe', category='simple', damage='1d6 slashing', price=5, weight=2,
                                 properties=['light', 'thrown (range 20/60)'])
        longbow = equipment.Weapon('longbow', category='martial', damage='1d8 piercing', price=50, weight=2,
                                   properties=['ammunition (range 150/600)', 'heavy', 'two-handed'])
        worn_items.don_armor(armor)
        worn_items.equip_weapon(rondel)
        worn_items.equip_weapon(lefon)
        worn_items.equip_weapon(longbow)
        return worn_items

    dorian_equip = generate_equipment()
    dorian_backpack = generate_backpack()
    dorian_pc = pc.PlayerCharacter(dorian_base, dorian_race, dorian_class, dorian_background, dorian_equip, dorian_backpack)
    return dorian_pc


def create_tamiphi(level=1):
    tamiphi_base = pc.PlayerBase("Tamiphi Tockentell", 10, 11, 15, 14, 16, 7, level=level)
    tam_race = race.RockGnome()
    class_languages = trait.LanguagesKnown(languages=[base.Languages.DRACONIC, base.Languages.DWARVISH])
    tam_class = cleric.Cleric(skill_proficiencies=[Skills.INSIGHT, Skills.RELIGION, Skills.ARCANA, Skills.PERSUASION],
                              languages=class_languages)
    if level > 1:
        tam_class.level_to(level=level,
                           fighting_style='two_weapon_fighting',
                           archetype_feature='colossus_slayer',
                           ability_score_increase={
                               base.AbilityScore.WIS: base.AbilityScoreIncrease(base.AbilityScore.WIS, 2),
                           })
    bg_languages = trait.LanguagesKnown(languages=[base.Languages.CELESTIAL, base.Languages.INFERNAL])
    tam_bg = background.Sage(bg_languages)

    def generate_backpack():
        backpack = equipment.Backpack(copper_pieces=0, silver_pieces=0, gold_pieces=10, platnium_pieces=0, items=None)
        return backpack

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

    tam_equip = generate_equipment()
    tam_backpack = generate_backpack()
    tamiphi_pc = pc.PlayerCharacter(tamiphi_base, tam_race, tam_class, tam_bg, tam_equip, tam_backpack)
    return tamiphi_pc


def create_fethri(level=1):
    fethri_base = pc.PlayerBase("Fethri Winterwhisper", 10, 14, 12, 15, 11, 12, level=level)
    tool_prof = [
        trait.ToolProficiency(name='Tool Proficiency',
                              proficiencies=['brewers_kit'])
    ]
    fethri_race = race.Tiefling(traits=tool_prof)
    fethri_class = rogue.Rogue(skill_proficiencies=[Skills.INVESTIGATION,
                                                    Skills.DECEPTION,
                                                    Skills.STEALTH],
                               expertise=trait.Expertise(skills=[Skills.INVESTIGATION,
                                                                 Skills.DECEPTION],
                                                         proficiencies=None)
                               )
    if level > 1:
        fethri_class.level_to(level=level,
                              gaming_set='bone_dice',
                              languages=trait.LanguagesKnown(languages=[base.Languages.CELESTIAL,
                                                                        base.Languages.DWARVISH]),
                              ability_score_increase={
                                  base.AbilityScore.INT: base.AbilityScoreIncrease(base.AbilityScore.INT, 2),
                              })
    fethri_bg = background.Noble(tool_proficiency=trait.ToolProficiency(proficiencies=['chess_set']),
                                 languages=trait.LanguagesKnown(languages=[base.Languages.DRACONIC]))

    def generate_backpack():
        logger.debug('Displaying equipment in backpack')
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

    def generate_equipment():
        logger.debug('Displaying worn items')
        worn_items = equipment.WornItems()

        def calc_light_armor_rating(dex_mod):
            # leather armor
            return 11 + dex_mod

        armor = equipment.Armor('Leather Armor', price=10, weight=10, armor_class=calc_light_armor_rating,
                                strength=0, stealth='')
        longbow = equipment.Weapon('longbow', category='martial', damage='1d8 piercing', price=50, weight=2,
                                   properties=['ammunition (range 150/600)', 'heavy', 'two-handed'])
        worn_items.don_armor(armor)
        worn_items.equip_weapon(longbow)
        return worn_items

    fethri_equipment = generate_equipment()
    fethri_backpack = generate_backpack()
    fethri_pc = pc.PlayerCharacter(fethri_base, fethri_race, fethri_class, fethri_bg, fethri_equipment, fethri_backpack)
    return fethri_pc
