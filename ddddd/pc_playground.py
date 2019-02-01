
import json

from ddddd.entity import base
from ddddd.entity.base import Skills, Languages
from ddddd.entity.character import race, cclass, background, pc, equipment
from ddddd.entity.character import trait

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def main():
    """
    Testing playground for D&D Infinity.
    """
    test_pc()
    print('bye')


def create_dorian():
    level = 5
    dorian_base = pc.PlayerBase("Dorian Sapbleden", 16, 10, 14, 12, 14, 8, level=level)
    # tool_prof = {
    #     'tool_proficiency': {
    #         'name': 'Tool Proficiency',
    #         'tools': [],
    #         'description': 'You gain proficiency with the artisan''s tools of your choice: smith''s tools, brewer''s supplies, or mason''s tools.',
    #     }
    # }
    tool_prof = [
        trait.ToolProficiency(name='Tool Proficiency',
                              proficiencies=['brewers_kit'])
    ]
    dorian_race = race.HillDwarf(traits=tool_prof)
    dorian_class = cclass.Ranger(skill_proficiencies=[Skills.ATHLETICS, Skills.ANIMAL_HANDLING, Skills.SURVIVAL],
                                 favored_enemy='plants',
                                 languages='elvish',
                                 favored_terrain='forest')
    dorian_class.level_to(level=level,
                          fighting_style='two_weapon_fighting',
                          archetype_feature='colossus_slayer',
                          ability_score_increase={'STR': 2})
    dorian_background = background.Criminal()
    dorian_equip = generate_equipment()
    dorian_backpack = generate_backpack()
    dorian_pc = pc.PlayerCharacter(dorian_base, dorian_race, dorian_class, dorian_background, dorian_equip, dorian_backpack)
    return dorian_pc


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
    backpack.add_item(equipment.Armor('Leather Armor', price=10, weight=10, armor_class=calc_light_armor_rating, strength=0, stealth=''))

    def calc_medium_armor_rating(dex_mod):
        # chain shirt
        return 13 + min(dex_mod, 2)
    backpack.add_item(equipment.Armor('Chain Shirt', price=50, weight=20, armor_class=calc_medium_armor_rating, strength=0, stealth=''))

    logger.debug(json.dumps(backpack.__json__(), indent=4))
    return backpack


def generate_equipment():
    logger.debug('Displaying worn items')
    worn_items = equipment.WornItems()

    def calc_heavy_armor_rating():
        # chain mail
        return 16
    armor = equipment.Armor('Chain Mail', price=75, weight=55, armor_class=calc_heavy_armor_rating, strength=15, stealth='disadvantage')
    rondel = equipment.Weapon('handaxe', damage='1d6 slashing', price=5, weight=2, properties=['light', 'thrown (range 20/60)'])
    lefon = equipment.Weapon('handaxe', damage='1d6 slashing', price=5, weight=2, properties=['light', 'thrown (range 20/60)'])
    longbow = equipment.Weapon('longbow', damage='1d8 piercing', price=50, weight=2, properties=['ammunition (range 150/600)', 'heavy', 'two-handed'])
    worn_items.don_armor(armor)
    worn_items.equip_weapon(rondel)
    worn_items.equip_weapon(lefon)
    worn_items.equip_weapon(longbow)
    logger.debug(json.dumps(worn_items.__json__(), indent=4))
    return worn_items


def test_pc():

    ttt_base = pc.PlayerBase("Tamiphi Tockentell", 10, 11, 16, 18, 20, 7, level=8)
    gnome = race.RockGnome()
    logger.info(ttt_base)
    logger.info(gnome)

    logger.info('-----')

    lok_base = pc.PlayerBase("Lok", 15, 18, 10, 12, 16, 9, level=4)
    human = race.Human(languages=[Languages.DRACONIC])
    logger.info(lok_base)
    logger.info(human)

    logger.info('-----')

    dorian_pc = create_dorian()
    # logger.info(json.dumps(dorian_pc.__json__(), indent=4))
    # req = dorian_pc.race.verify()
    # logger.info(req)

    # print('-----')
    #
    # print(json.dumps(dorian_pc.generate_character_sheet(), indent=4))


if __name__ == '__main__':
    main()

