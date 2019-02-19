import unittest
from ddddd.items import currency


class TestBasicCurrencies(unittest.TestCase):
    def test_copper_pieces(self):
        cp = currency.CopperPieces(1000)
        self.assertEqual(1000, cp.amt)
        self.assertEqual(currency.CopperPieces(1000), cp.copper_conversion())

    def test_silver_pieces(self):
        sp = currency.SilverPieces(100)
        self.assertEqual(100, sp.amt)
        self.assertEqual(currency.CopperPieces(1000), sp.copper_conversion())

    def test_gold_pieces(self):
        gp = currency.GoldPieces(10)
        self.assertEqual(10, gp.amt)
        self.assertEqual(currency.CopperPieces(1000), gp.copper_conversion())

    def test_platinum_pieces(self):
        pp = currency.PlatinumPieces(1)
        self.assertEqual(1, pp.amt)
        self.assertEqual(currency.CopperPieces(1000), pp.copper_conversion())


class TestConversionFunctions(unittest.TestCase):
    def test_convert_to_copper(self):
        money = [
            currency.CopperPieces(1000),
            currency.SilverPieces(100),
            currency.GoldPieces(10),
            currency.PlatinumPieces(1),
        ]
        self.assertEqual(currency.CopperPieces(4000), currency.convert_to_copper(money))

    def test_convert_to_gold(self):
        money = [
            currency.CopperPieces(1000),
            currency.SilverPieces(100),
            currency.GoldPieces(10),
            currency.PlatinumPieces(1),
        ]
        self.assertEqual(currency.GoldPieces(40), currency.convert_to_gold(money))


class TestMoneyPouch(unittest.TestCase):
    def test_no_money(self):
        pouch = currency.MoneyPouch()

        self.assertEqual(pouch.money['CP'].amt, 0)
        self.assertEqual(pouch.money['SP'].amt, 0)
        self.assertEqual(pouch.money['GP'].amt, 0)
        self.assertEqual(pouch.money['PP'].amt, 0)

        self.assertEqual(currency.CopperPieces(0), pouch.total_copper)

        self.assertEqual(currency.GoldPieces(0), pouch.total_gold)

    def test_with_money(self):
        pouch = currency.MoneyPouch(cp=currency.CopperPieces(1000),
                                    sp=currency.SilverPieces(100),
                                    gp=currency.GoldPieces(10),
                                    pp=currency.PlatinumPieces(1))
        self.assertEqual(pouch.money['CP'].amt, 1000)
        self.assertEqual(pouch.money['SP'].amt, 100)
        self.assertEqual(pouch.money['GP'].amt, 10)
        self.assertEqual(pouch.money['PP'].amt, 1)

        self.assertEqual(currency.CopperPieces(4000), pouch.total_copper)

    def test_add_money(self):
        pouch = currency.MoneyPouch()
        pouch.add(currency.CopperPieces(1000))
        pouch.add(currency.SilverPieces(100))
        pouch.add(currency.GoldPieces(10))
        pouch.add(currency.PlatinumPieces(1))

        self.assertEqual(pouch.money['CP'].amt, 1000)
        self.assertEqual(pouch.money['SP'].amt, 100)
        self.assertEqual(pouch.money['GP'].amt, 10)
        self.assertEqual(pouch.money['PP'].amt, 1)

        self.assertEqual(currency.CopperPieces(4000), pouch.total_copper)
