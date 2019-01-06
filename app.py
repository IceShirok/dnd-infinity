
import json
import sys

from base import Jsonable, PlayerBase
from race import HillDwarf, RockGnome, Human
from pclass import RangerFactory
from background import Criminal
from pc import PlayerCharacter

import equipment

from sheet import CharacterSheetGenerator

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

def test_pc():
    base = PlayerBase("Dorian Sapbleden", 16, 10, 14, 12, 14, 8, level=2)
    race = HillDwarf({})
    classes = [
            RangerFactory().generate_by_level(1),
            RangerFactory().generate_by_level(2)
            ]
    background = Criminal()
    pc = PlayerCharacter(base, race, classes, background)
    print(pc.__str__())

    print('-----')

    ttt_base = PlayerBase("Tamiphi Tockentell", 10, 11, 16, 18, 20, 7, level=8)
    gnome = RockGnome({})
    print(ttt_base)
    print(gnome)

    print('-----')

    lok_base = PlayerBase("Lok", 15, 18, 10, 12, 16, 9, level=4)
    human = Human()
    print(lok_base)
    print(human)
    #print('-----')

    #csheet = CharacterSheetGenerator().generate_character_sheet(pc)
    #print(json.dumps(csheet, indent=4))

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

