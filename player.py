class Player:
	def __init__(self):
		self.hand = []
		self.points = []
		self.faceCards = []

	def printHand(self):
		print("Hand:")
		for card in self.hand:
			print(card.name())

	def printField(self):
		print("Points:")
		for card in self.points:
			print(card.name())
		print("Face Cards:")
		for card in self.faceCards:
			print(card.name())

	def print(self):
		self.printHand()
		self.printField()

	# Returns how many queens player has on field
	def queenCount(self):
		res = 0
		for card in self.faceCards:
			if card.rank == 12:
				res += 1
		return res

	# Returns how many kings player has on field
	def kingCount(self):
		res = 0
		for card in self.faceCards:
			if card.rank == 13:
				res += 1
		return res

	# Returns player's current point total
	def totalPoints(self):
		res = 0
		for card in self.points:
			res += card.rank
		return res

	# Returns number of two's in hand
	def twosInHand(self):
		res = 0
		for card in self.hand:
			if card.rank == 2:
				res += 1
		return res

	def indexOfTwo(self):
		res = None
		for i, card in enumerate(self.hand):
			if card.rank == 2:
				res = i
		return res

	def couldWinNextTurn(self):
		if self.kingCount() == 0:
			return self.totalPoints() >= 11
		elif self.kingCount() == 1:
			return self.totalPoints() >= 4
		elif self.kingCount() == 2:
			return True
	# Returns whether player has won (boolean)
	def wins(self):
		if self.kingCount() == 0:
			return self.totalPoints() >= 21
		elif self.kingCount() == 1:
			return self.totalPoints() >= 14
		elif self.kingCount() == 2:
			return self.totalPoints() >= 10
		elif self.kingCount() == 3:
			return self.totalPoints() >= 7
		else:
			return self.totalPoints() >= 5