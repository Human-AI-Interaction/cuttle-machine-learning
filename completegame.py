from game import Game
# Class stores complete history of a game
class CompleteGame:
	def __init__(self):
		self.gameStates = [Game()]
		self.result = None

	def print(self):
		print("Initial Game State:")
		for game in self.gameStates:
			game.print()
		print("WINNER: %s" %self.gameStates[-1].winner())

	# Returns winner index from most recent game state
	def winner(self):
		return self.gameStates[-1].winner()
