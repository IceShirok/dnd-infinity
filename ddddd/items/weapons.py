from ddddd.entity.character import base
from ddddd.items import currency
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

LIGHT = 'light'
FINESSE = 'finesse'
HEAVY = 'heavy'
TWO_HANDED = 'two-handed'
AMMUNITION = 'ammunition'
THROWN = 'thrown'

#############################
# WEAPONS
#############################

MACE = Weapon('mace', category=SIMPLE, damage='1d6 bludgeoning',
              price=currency.GoldPieces(5), weight=4,
              properties=[])

HANDAXE = Weapon('handaxe', category=SIMPLE, damage='1d6 slashing',
                 price=currency.GoldPieces(5), weight=2,
                 properties=[LIGHT, 'thrown (range 20/60)'])

SHORTBOW = Weapon('shortbow', category=SIMPLE, damage='1d6 piercing',
                 price=currency.GoldPieces(10), weight=2,
                 properties=['ammunition (range 80/320)', TWO_HANDED])

RAPIER = Weapon('rapier', category=MARTIAL, damage='1d8 piercing',
                price=currency.GoldPieces(25), weight=2,
                properties=[FINESSE])

LONGBOW = Weapon('longbow', category=MARTIAL, damage='1d8 piercing',
                 price=currency.GoldPieces(50), weight=2,
                 properties=['ammunition (range 150/600)', HEAVY, TWO_HANDED])

LONGSWORD = Weapon('lsongsword', category=MARTIAL, damage='1d8 piercing',
                   price=currency.GoldPieces(15), weight=3,
                   properties=['versatile (1d10)'])

WEAPON_TYPE_TO_WEAPONS = {
    SIMPLE: [MACE, HANDAXE, SHORTBOW],
    MARTIAL: [RAPIER, LONGBOW],
}


def get_aggregated_weapon_proficiencies(proficiencies):
    prof_agg = proficiencies
    if SIMPLE in proficiencies and MARTIAL in proficiencies:
        return [SIMPLE, MARTIAL]
    elif SIMPLE in proficiencies:
        for weapon in WEAPON_TYPE_TO_WEAPONS[SIMPLE]:
            if weapon.name in prof_agg:
                prof_agg.remove(weapon.name)
        return prof_agg
    elif MARTIAL in proficiencies:
        for weapon in WEAPON_TYPE_TO_WEAPONS[MARTIAL]:
            if weapon.name in prof_agg:
                prof_agg.remove(weapon.name)
        return prof_agg
    return prof_agg


def determine_attack_bonus_type(weapon, ability_scores):
    str_mod = (base.AbilityScore.STR, ability_scores[base.AbilityScore.STR].modifier)
    dex_mod = (base.AbilityScore.DEX, ability_scores[base.AbilityScore.DEX].modifier)

    attack_mod = str_mod
    for w_prop in weapon.properties:
        w_prop = w_prop.lower()
        if AMMUNITION in w_prop:  # Weapon is ranged only
            attack_mod = dex_mod
        elif FINESSE in w_prop:  # Weapon is finesse
            attack_mod = dex_mod if dex_mod[1] > str_mod[1] else str_mod
    return attack_mod


def is_proficient(weapon, weapon_proficiencies):
    return weapon.category.lower() in weapon_proficiencies or weapon.name.lower() in weapon_proficiencies
