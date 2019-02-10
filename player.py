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

	def queenCount(self):
		res = 0
		for card in self.faceCards:
			if card.rank == 12:
				res += 1
		return res

	def kingCount(self):
		res = 0
		for card in self.faceCards:
			if card.rank == 13:
				res += 1
		return res

	def totalPoints(self):
		res = 0
		for card in self.points:
			res += card.rank
		return res

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