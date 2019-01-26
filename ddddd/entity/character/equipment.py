

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

    def __json__(self):
        weapons_p = []
        for i in self.weapons:
            weapons_p.append(i.__json__())
        j = {
            'weapons': weapons_p,
            'armor': self.armor.__json__() if self.armor else 'none',
            'total_weight': self.total_weight,
        }
        return j


class Backpack(object):
    """
    A player character's (PC) backpack, or equipment.
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
        self.copper_pieces = copper_pieces
        self.silver_pieces = silver_pieces
        self.gold_pieces = gold_pieces
        self.platnium_pieces = platnium_pieces

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
        total = 0
        for item in self.items:
            total += (item.price * item.quantity)
        return total

    def __json__(self):
        items_p = []
        for i in self.items:
            items_p.append(i.__json__())
        j = {
            'money': {
                'CP': self.copper_pieces,
                'SP': self.silver_pieces,
                'GP': self.gold_pieces,
                'PP': self.platnium_pieces,
            },
            'total_weight': self.total_weight,
            'total_item_worth': self.total_item_worth,
            'items': items_p,
        }
        return j


class Item(object):
    """
    An item in D&D.
    The price will assume that it is in copper pieces (CP),
    since that is the lowest denomination of money.
    Weight is in pounds (lbs).
    Quantity is used if the item is atomic. i.e. candles are
    either usable or not usable. Healing kits have number of uses.
    """
    def __init__(self, name, price=0, weight=0, description=None, quantity=1):
        self.name = name
        self.description = description
        self.price = price
        self.weight = weight
        self.quantity = quantity

    def __json__(self):
        j = {
            'name': self.name,
            'price': self.price,
            'weight': self.weight,
        }
        if self.description:
            j['description'] = self.description
        if self.quantity > 1:
            j['quantity'] = self.quantity
        return j


class Weapon(Item):
    """
    Weapon in D&D.
    Weapons are simple or martial weapons.
    Weapons can have many different properties and damage.
    """
    def __init__(self, name, damage, price, weight, properties):
        super(Weapon, self).__init__(name, price, weight)
        self.damage = damage
        self.properties = properties

    def __json__(self):
        j = {
            **super(Weapon, self).__json__(),
            'damage': self.damage,
            'properties': self.properties,
        }
        return j


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
