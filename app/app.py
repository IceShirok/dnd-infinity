
import json
import sys

import race, cclass, background, pc
import equipment

"""
Testing playground for D&D Infinity.
"""
def main():
    if len(sys.argv) < 2:
        print('put in argument pls')
        print('"pc" for testing pc')
        print('"stuff" for testing equipment')
    elif sys.argv[1] == 'pc':
        test_pc()
    elif sys.argv[1] == 'stuff':
        test_stuff()
    else:
        print('not sure what you put in')
        print('try something else')
    print('bye')

def create_dorian():
    dorian_base = pc.PlayerBase("Dorian Sapbleden", 16, 10, 14, 12, 14, 8, level=2)
    tool_prof = {
        'tool_proficiency': {
            'name': 'Tool Proficiency',
            'tools': ['brewers_kit'],
            'description': 'You gain proficiency with the artisan’s tools of your choice: smith’s tools, brewer’s supplies, or mason’s tools.',
        }
    }
    dorian_race = race.HillDwarf(traits=tool_prof)
    dorian_classes = [
            cclass.RangerFactory().generate_by_level(1, skills=['athletics', 'animal_handling', 'survival'], favored_enemy='plants', languages='elvish', favored_terrain='forest'),
            cclass.RangerFactory().generate_by_level(2, fighting_style=['two_weapon_fighting'])
            ]
    dorian_background = background.Criminal()
    dorian_pc = pc.PlayerCharacter(dorian_base, dorian_race, dorian_classes, dorian_background)
    return dorian_pc

def test_pc():
    dorian_pc = create_dorian()
    print(dorian_pc.__str__())

    print('-----')

    ttt_base = pc.PlayerBase("Tamiphi Tockentell", 10, 11, 16, 18, 20, 7, level=8)
    gnome = race.RockGnome()
    print(ttt_base)
    print(gnome)

    print('-----')

    lok_base = pc.PlayerBase("Lok", 15, 18, 10, 12, 16, 9, level=4)
    human = race.Human(languages=['draconic'])
    print(lok_base)
    print(human)

    print('-----')

    print(json.dumps(dorian_pc.generate_character_sheet(), indent=4))

def test_stuff():
    backpack = equipment.Backpack(gold_pieces=15)
    print(backpack)
    backpack.add_item(equipment.Weapon('dagger', '1d4 piercing', 200, 1, ['finesse', 'light', 'thrown (range 20/60)'])
)
    backpack.add_item(equipment.Item('crowbar'))
    backpack.add_item(equipment.Item('clothes', description='A set of dark common clothes including a hood.'))
    print(backpack)

if __name__ == '__main__':
    main()

