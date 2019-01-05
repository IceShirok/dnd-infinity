
from base import Jsonable

class Backpack(Jsonable):
    def __init__(self):
	self.copper_pieces = 0
	self.silver_pieces = 0
	self.gold_pieces = 0
	self.platnium_pieces = 0

	self.items = []

    def __json__(self):
	j = {
	    'money': {
		'CP': self.copper_pieces,
		'SP': self.silver_pieces,
		'GP': self.gold_pieces,
		'PP': self.platnium_pieces,
	    },
	    'items': self.items,
	}
	return j

