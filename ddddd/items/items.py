from ddddd.items import currency
from ddddd.items.currency import CopperPieces, SilverPieces, GoldPieces


class Item(object):
    """
    An item in D&D.
    The price will assume that it is in copper pieces (CP),
    since that is the lowest denomination of money.
    Weight is in pounds (lbs).
    Quantity is used if the item is atomic. i.e. candles are
    either usable or not usable. Healing kits have number of uses.
    """
    def __init__(self, name, price=None, weight=0, description=None, quantity=1):
        self.name = name
        self.description = description
        self.price = price if price else CopperPieces(0)
        self.weight = weight
        self.quantity = quantity


#############################
# EQUIPMENT PACKS
#############################

class WornItems(object):
    """
    The items that are currently equipped on the
    player character (PC). This differs from the backpack,
    whose purpose is to list
    """
    def __init__(self,
                 armor=None,
                 weapons=None):
        self.armor = armor
        self.weapons = weapons if weapons else []

    def don_armor(self, armor):
        doffed = None
        if self.armor:
            doffed = self.doff_armor()
        self.armor = armor
        return doffed

    def doff_armor(self):
        doffed = self.armor
        self.armor = None
        return doffed

    def equip_weapon(self, weapon):
        self.weapons.append(weapon)
        return None

    def unequip_weapon(self, weapon_name):
        doffed = None
        for weapon in self.weapons:
            if weapon.name == weapon_name:
                doffed = weapon
        if doffed:
            self.weapons.remove(doffed)
        return doffed

    @property
    def total_weight(self):
        total = 0
        total += self.armor.weight if self.armor else 0
        for weapon in self.weapons:
            total += weapon.weight
        return total

    @property
    def total_item_worth(self):
        total = []
        if self.armor:
            total.append(self.armor.price)
        for weapon in self.weapons:
            total.append(weapon.price)
        return currency.convert_to_gold(total).amt


class Backpack(object):
    """
    A player character's (PC) backpack, or 
    Currently a work-in-progress, since this particular
    feature is much more transient than a PC's stats.
    The 'trasient' feature will likely is delegated to
    a specific service.
    """
    def __init__(self,
                 copper_pieces=0,
                 silver_pieces=0,
                 gold_pieces=0,
                 platnium_pieces=0,
                 items=None):
        self.money_pouch = currency.MoneyPouch(currency.CopperPieces(copper_pieces),
                                               currency.SilverPieces(silver_pieces),
                                               currency.GoldPieces(gold_pieces),
                                               currency.PlatinumPieces(platnium_pieces))

        self.items = items if items else []

    def add_item(self, item):
        self.items.append(item)

    @property
    def total_weight(self):
        total = 0
        for item in self.items:
            total += (item.weight * item.quantity)
        return total

    @property
    def total_item_worth(self):
        total = list(self.money_pouch.money.values())
        for item in self.items:
            for i in range(0, item.quantity):
                total.append(item.price)
        return currency.convert_to_gold(total).amt


#############################
# FULLY-STOCKED PACKS
#############################

def generate_explorers_pack():
    backpack = Backpack(copper_pieces=0, silver_pieces=0, gold_pieces=10, platnium_pieces=0, items=None)
    backpack.add_item(Item('Bedroll', price=GoldPieces(1), weight=7))
    backpack.add_item(Item('Mess Kit', price=GoldPieces(1), weight=1))
    backpack.add_item(Item('Tinderbox', price=GoldPieces(1), weight=1))
    backpack.add_item(Item('Torches', price=GoldPieces(1), weight=0, quantity=10))
    backpack.add_item(Item('Rations', price=SilverPieces(5), weight=2, quantity=10))
    backpack.add_item(Item('Waterskin', price=GoldPieces(1), weight=5))
    backpack.add_item(Item('Hempen Rope', price=GoldPieces(1), weight=10, description='50 ft of rope'))
    return backpack


def generate_burglars_pack():
    backpack = Backpack(copper_pieces=0, silver_pieces=0, gold_pieces=10, platnium_pieces=0, items=None)
    backpack.add_item(Item('Ball Bearings', price=GoldPieces(1), weight=2))
    backpack.add_item(Item('String', price=SilverPieces(2), weight=0, description='10 ft of string'))
    backpack.add_item(Item('Bell', price=GoldPieces(1), weight=0))
    backpack.add_item(Item('Candle', price=SilverPieces(2), weight=0, quantity=5))
    backpack.add_item(Item('Crowbar', price=GoldPieces(2), weight=5, quantity=2))
    backpack.add_item(Item('Hammer', price=GoldPieces(1), weight=3))
    backpack.add_item(Item('Piton', price=SilverPieces(2), weight=1, quantity=10))
    backpack.add_item(Item('Hooded Lantern', price=GoldPieces(4), weight=2))
    backpack.add_item(Item('Flask of Oil', price=GoldPieces(1), weight=1, quantity=2))
    backpack.add_item(Item('Rations', price=SilverPieces(5), weight=2, quantity=5))
    backpack.add_item(Item('Tinderbox', price=GoldPieces(1), weight=1))
    backpack.add_item(Item('Waterskin', price=GoldPieces(1), weight=5))
    backpack.add_item(Item('Hempen Rope', price=GoldPieces(1), weight=10, description='50 ft of rope'))
    return backpack
