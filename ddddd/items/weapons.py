
from ddddd.items.items import Item


class Weapon(Item):
    """
    Weapon in D&D.
    Weapons are simple or martial weapons.
    Weapons can have many different properties and damage.
    """
    def __init__(self, name, category, damage, price, weight, properties):
        super(Weapon, self).__init__(name, price, weight)
        self.category = category
        self.damage = damage
        self.properties = properties


#############################
# WEAPONS
#############################

MACE = Weapon('Mace', category='simple', damage='1d6 bludgeoning',
              price=5, weight=4,
              properties=[])

HANDAXE = Weapon('Handaxe', category='simple', damage='1d6 slashing',
                 price=5, weight=2,
                 properties=['light', 'thrown (range 20/60)'])

RAPIER = Weapon('Rapier', category='martial', damage='1d8 piercing',
                price=25, weight=2,
                properties=['finesse'])

LONGBOW = Weapon('Longbow', category='martial', damage='1d8 piercing',
                 price=50, weight=2,
                 properties=['ammunition (range 150/600)', 'heavy', 'two-handed'])
