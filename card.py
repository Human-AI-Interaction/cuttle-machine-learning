class Card:
	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank
		self.jacks = []

	def name(self):
		if self.suit == 0:
			suit = " of Clubs"
		elif self.suit == 1:
			suit = " of Diamonds"
		elif self.suit == 2:
			suit = " of Hearts"
		else:
			suit = " of Spades"
		return "%s%s" %(self.rank, suit)
	
