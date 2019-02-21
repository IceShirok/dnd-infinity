import unittest
from ddddd.items import armor, items, weapons, currency


class TestWornItems(unittest.TestCase):
    def setUp(self):
        self.worn_items = items.WornItems()

    def test_don_armor_from_nothing(self):
        self.assertEqual(None, self.worn_items.armor)
        a = armor.LEATHER_ARMOR
        self.worn_items.don_armor(a)
        self.assertEqual(a, self.worn_items.armor)

    def test_doff_armor_from_something(self):
        a = armor.LEATHER_ARMOR
        self.worn_items = items.WornItems(armor=a)
        self.assertEqual(a, self.worn_items.armor)

        doffed = self.worn_items.doff_armor()
        self.assertEqual(a, doffed)
        self.assertEqual(None, self.worn_items.armor)

    def test_don_armor_from_something(self):
        a = armor.LEATHER_ARMOR
        self.worn_items = items.WornItems(armor=a)

        b = armor.CHAIN_SHIRT
        doffed = self.worn_items.don_armor(b)
        self.assertEqual(a, doffed)
        self.assertEqual(b, self.worn_items.armor)

    def test_doff_armor_from_nothing(self):
        doffed = self.worn_items.doff_armor()
        self.assertEqual(None, doffed)
        self.assertEqual(None, self.worn_items.armor)

    def test_equip_weapon(self):
        self.assertEqual(0, len(self.worn_items.weapons))

        self.worn_items.equip_weapon(weapons.MACE)
        self.worn_items.equip_weapon(weapons.RAPIER)
        self.assertEqual(2, len(self.worn_items.weapons))

    def test_unequip_weapon(self):
        mace = weapons.MACE
        rapier = weapons.RAPIER
        self.worn_items.equip_weapon(mace)
        self.worn_items.equip_weapon(rapier)
        self.assertEqual(2, len(self.worn_items.weapons))

        unequipped = self.worn_items.unequip_weapon('mace')
        self.assertEqual(1, len(self.worn_items.weapons))
        self.assertEqual(mace, unequipped)
        self.assertTrue(rapier in self.worn_items.weapons)

    def test_total_weight(self):
        self.assertEqual(0, self.worn_items.total_weight)

        a = armor.LEATHER_ARMOR
        self.worn_items.don_armor(a)
        self.assertEqual(10, self.worn_items.total_weight)

        mace = weapons.MACE
        rapier = weapons.RAPIER
        self.worn_items.equip_weapon(mace)
        self.worn_items.equip_weapon(rapier)
        self.assertEqual(16, self.worn_items.total_weight)

    def test_total_item_worth(self):
        self.assertEqual(0, self.worn_items.total_item_worth)

        a = armor.LEATHER_ARMOR
        self.worn_items.don_armor(a)
        self.assertEqual(10, self.worn_items.total_item_worth)

        mace = weapons.MACE
        rapier = weapons.RAPIER
        self.worn_items.equip_weapon(mace)
        self.worn_items.equip_weapon(rapier)
        self.assertEqual(40, self.worn_items.total_item_worth)


class TestBackpack(unittest.TestCase):
    def setUp(self):
        self.backpack = items.Backpack()

    def test_add_item(self):
        self.assertEqual(0, len(self.backpack.items))

        item = items.Item('Bedroll', price=currency.GoldPieces(1), weight=7)
        for i in range(0, 10):
            self.backpack.add_item(item)
        self.assertEqual(10, len(self.backpack.items))

        # We'll consider a "package" of stuffs to be a singular unit
        # As in, some items (i.e. bag of ball bearings) would make more sense
        # if they were grouped together as one unit.
        item = items.Item('Torches', price=currency.GoldPieces(1), weight=1, quantity=10)
        for i in range(0, 10):
            self.backpack.add_item(item)
        self.assertEqual(20, len(self.backpack.items))

    def test_total_weight(self):
        self.assertEqual(0, self.backpack.total_weight)

        item = items.Item('Bedroll', price=currency.GoldPieces(1), weight=7)
        for i in range(0, 10):
            self.backpack.add_item(item)
        self.assertEqual(70, self.backpack.total_weight)

        # We'll consider a "package" of stuffs to be a singular unit
        # As in, some items (i.e. bag of ball bearings) would make more sense
        # if they were grouped together as one unit.
        item = items.Item('Torches', price=currency.GoldPieces(1), weight=1, quantity=10)
        for i in range(0, 10):
            self.backpack.add_item(item)
        self.assertEqual(170, self.backpack.total_weight)

    def test_total_item_worth(self):
        self.assertEqual(0, self.backpack.total_item_worth)

        item = items.Item('Bedroll', price=currency.GoldPieces(1), weight=7)
        for i in range(0, 10):
            self.backpack.add_item(item)
        self.assertEqual(10, self.backpack.total_item_worth)

        # This is a bit strange because some items are priced by unit
        # and others are priced by a bundle.
        # This is something that should be nailed down...
        item = items.Item('Torches', price=currency.SilverPieces(1), weight=1, quantity=10)
        for i in range(0, 10):
            self.backpack.add_item(item)
        self.assertEqual(20, self.backpack.total_item_worth)
