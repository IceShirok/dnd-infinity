
class Currency(object):
    def __init__(self, amt):
        self.amt = amt

    @property
    def type_(self):
        raise NotImplementedError()

    def __eq__(self, other):
        if isinstance(other, Currency):
            return self.amt == other.amt
        return False

    def __str__(self):
        return '{}{}'.format(self.amt, self.type_)


class CopperPieces(Currency):
    def __init__(self, amt):
        super(CopperPieces, self).__init__(amt)

    @property
    def type_(self):
        return 'CP'

    def copper_conversion(self):
        return CopperPieces(self.amt * 1)

    def gold_conversion(self):
        """Converts copper to gold, rounded down."""
        return GoldPieces(self.amt // 100)


class SilverPieces(Currency):
    def __init__(self, amt):
        super(SilverPieces, self).__init__(amt)

    @property
    def type_(self):
        return 'SP'

    def copper_conversion(self):
        return CopperPieces(self.amt * 10)


class GoldPieces(Currency):
    def __init__(self, amt):
        super(GoldPieces, self).__init__(amt)

    @property
    def type_(self):
        return 'GP'

    def copper_conversion(self):
        return CopperPieces(self.amt * 100)


class PlatinumPieces(Currency):
    def __init__(self, amt):
        super(PlatinumPieces, self).__init__(amt)

    @property
    def type_(self):
        return 'PP'

    def copper_conversion(self):
        return CopperPieces(self.amt * 1000)


def convert_to_copper(money):
    return CopperPieces(sum(map(lambda c: c.copper_conversion().amt, money)))


def convert_to_gold(money):
    """Returns the total gold amount, rounded down."""
    return convert_to_copper(money).gold_conversion()


class MoneyPouch(object):
    """
    This class will simply hold onto coins as though
    holding physical coins. This class can also calculate
    the money amount.
    """
    def __init__(self, cp=None, sp=None, gp=None, pp=None):
        self.money = {
            'CP': cp if cp and isinstance(cp, CopperPieces) else CopperPieces(0),
            'SP': sp if sp and isinstance(sp, SilverPieces) else SilverPieces(0),
            'GP': gp if gp and isinstance(gp, GoldPieces) else GoldPieces(0),
            'PP': pp if pp and isinstance(pp, PlatinumPieces) else PlatinumPieces(0),
        }

    @property
    def total_copper(self):
        return convert_to_copper(self.money.values())

    @property
    def total_gold(self):
        return convert_to_gold(self.money.values())

    def add(self, money):
        self.money[money.type_].amt = self.money[money.type_].amt + money.amt
