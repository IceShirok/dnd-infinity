
from ddddd.items.items import Item


class Armor(Item):
    """
    Armor in D&D.
    Armor are light, medium, or heavy, or a shield.
    They have different prerequisites and effects.
    """
    def __init__(self, name, price, weight, armor_class, strength, stealth):
        super(Armor, self).__init__(name, price, weight)
        self.armor_class = armor_class
        self.strength = strength
        self.stealth = stealth


#############################
# ARMOR CLASS FUNCTIONS
#############################

def calc_light_armor_rating(dex_mod):
    # leather armor
    return 11 + dex_mod


def calc_medium_armor_rating(dex_mod):
    # chain shirt
    return 13 + min(dex_mod, 2)


def calc_heavy_armor_rating():
    # chain mail
    return 16


#############################
# ARMOR
#############################

LEATHER_ARMOR = Armor('Leather Armor', price=10, weight=10,
                      armor_class=calc_light_armor_rating,
                      strength=0, stealth='')

CHAIN_SHIRT = Armor('Chain Shirt', price=50, weight=20,
                    armor_class=calc_medium_armor_rating,
                    strength=0, stealth='')

CHAIN_MAIL = Armor('Chain Mail', price=75, weight=55,
                   armor_class=calc_heavy_armor_rating,
                   strength=15, stealth='disadvantage')
