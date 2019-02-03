
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
# CONSTANTS
#############################

SIMPLE = 'simple'
MARTIAL = 'martial'

#############################
# WEAPONS
#############################

MACE = Weapon('Mace', category=SIMPLE, damage='1d6 bludgeoning',
              price=5, weight=4,
              properties=[])

HANDAXE = Weapon('Handaxe', category=SIMPLE, damage='1d6 slashing',
                 price=5, weight=2,
                 properties=['light', 'thrown (range 20/60)'])

RAPIER = Weapon('Rapier', category=MARTIAL, damage='1d8 piercing',
                price=25, weight=2,
                properties=['finesse'])

LONGBOW = Weapon('Longbow', category=MARTIAL, damage='1d8 piercing',
                 price=50, weight=2,
                 properties=['ammunition (range 150/600)', 'heavy', 'two-handed'])

WEAPON_TYPE_TO_WEAPONS = {
    SIMPLE: [MACE, HANDAXE],
    MARTIAL: [RAPIER, LONGBOW],
}


def get_aggregated_weapon_proficiencies(proficiencies):
    prof_agg = proficiencies
    if SIMPLE in proficiencies and MARTIAL in proficiencies:
        return [SIMPLE, MARTIAL]
    elif SIMPLE in proficiencies:
        for weapon in WEAPON_TYPE_TO_WEAPONS[SIMPLE]:
            if weapon in prof_agg:
                prof_agg.remove(weapon.name)
        return prof_agg
    elif MARTIAL in proficiencies:
        for weapon in WEAPON_TYPE_TO_WEAPONS[MARTIAL]:
            if weapon in prof_agg:
                prof_agg.remove(weapon.name)
        return prof_agg
    return prof_agg
