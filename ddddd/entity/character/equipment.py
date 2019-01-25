
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
            'items': items_p,
        }
        return j


class Item(object):
    """
    An item in D&D.
    The price will assume that it is in copper pieces (CP),
    since that is the lowest denomination of money.
    Weight is in pounds (lbs).
    """
    def __init__(self, name, price=0, weight=0, description=None):
        self.name = name
        self.description = description
        self.price = price
        self.weight = weight

    def __json__(self):
        j = {
            'name': self.name,
        }
        if self.description:
            j['description'] = self.description
        if self.price > 0:
            j['price'] = self.price
        if self.weight > 0:
            j['weight'] = self.weight
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
