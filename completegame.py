class CompleteGame:
	def __init__(self):
		self.gameStates = []
		self.winnerIndex = None

	def print(self):
		for game in self.gameStates:
			game.print()