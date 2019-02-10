from card import Card
from player import Player
from random import shuffle

class Game:
	def __init__(self):
		self.players = []
		self.deck = []
		self.scrap = []
		self.turn = 0
		self.oneOff = None

		# Initialize deck
		for i in range(4):
			for j in range(1,14):
				self.deck.append(Card(i, j))

		# Create players
		self.players.append(Player())
		self.players.append(Player())

		# deal
		shuffle(self.deck)
		self.players[1].hand.append(self.deck.pop(-1))
		for i in range(5):
			self.players[0].hand.append(self.deck.pop(-1))
			self.players[1].hand.append(self.deck.pop(-1))


	def print(self):
		for i, player in enumerate(self.players):
			print("\nPlayer %s's hand:" %i)
			player.printHand()

# blarg = Game()
# blarg.print()



