class Card:
	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank
		self.jacks = []
		self.frozen = False

	# Return string name of card
	def name(self):
		rank = self.rank
		if rank == 1:
			rank = "Ace"
		elif rank == 11:
			rank = "Jack"
		elif rank == 12:
			rank = "Queen"
		elif rank == 13:
			rank = "King"

		if self.suit == 0:
			suit = " of Clubs"
		elif self.suit == 1:
			suit = " of Diamonds"
		elif self.suit == 2:
			suit = " of Hearts"
		else:
			suit = " of Spades"
		return "%s%s" %(rank, suit)
	
