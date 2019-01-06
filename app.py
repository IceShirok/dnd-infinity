
import json

from base import Jsonable, PlayerBase
from race import HillDwarf, RockGnome, Human
from pclass import RangerFactory
from background import Criminal
from pc import PlayerCharacter

from sheet import CharacterSheetGenerator

def main():
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


if __name__ == '__main__':
    main()

