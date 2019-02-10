class Player:
	def __init__(self):
		self.hand = []
		self.points = []
		self.faceCards = []

	def printHand(self):
		for card in self.hand:
			print(card.name())