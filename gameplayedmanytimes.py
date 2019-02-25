from copy import deepcopy
from random import randint
from completegame import CompleteGame


# Returns the result of playing a given card as a oneOff
	# Returns array of possible results (in case card can be played multiple ways)
def playCardAsOneOff(originalGame, pIndex, cIndex):
	res = []
	counterResult = deepcopy(originalGame)
	card = counterResult.players[pIndex].hand.pop(cIndex)
	counterResult.scrap.append(card)
	worlds_where_oneOff_resovlves = [deepcopy(counterResult)]
	# Add cases where twos are played as possible results
	twoIndex = counterResult.players[(pIndex + 1) % 2].indexOfTwo()
	if counterResult.players[pIndex].queenCount == 0 and twoIndex != None:
		# counterResult.scrap.append(counterResult.players[pIndex].hand.pop(cIndex))
		counterResult.scrap.append(counterResult.players[(pIndex + 1) % 2].hand.pop(twoIndex))
		counterResult.log.append("Player %s plays the %s as a oneOff but is countered by the %s" %(pIndex, card.name(), counterResult.scrap[-1]))
		res.append(deepcopy(counterResult))

		# Add cases where player counters back
		twoIndex = counterResult.players[pIndex].indexOfTwo()
		if counterResult.players[(pIndex + 1) % 2].queenCount() == 0 and twoIndex != None:
			counterResult.scrap.append(counterResult.players[pIndex].hand.pop(twoIndex))
			counterResult.log.append("Player %s counters back with the %s" %(pIndex, counterResult.scrap[-1].name()))
			worlds_where_oneOff_resovlves.append(deepcopy(counterResult))


			# Opponent counters back again (3 twos stacked)
			twoIndex = counterResult.players[(pIndex + 1) % 2].indexOfTwo()
			if twoIndex != None:
				counterResult.scrap.append(counterResult.players[(pIndex + 1) % 2].hand.pop(twoIndex))
				counterResult.log.append("Player %s stacks 3rd counter with the %s" %(pIndex, counterResult.scrap[-1].name()))
				res.append(deepcopy(counterResult))

			# Player makes final counter (all 4 2's) to resolve oneOff
				twoIndex = counterResult.players[pIndex].indexOfTwo()
				if twoIndex != None:
					counterResult.scrap.append(game.players[pIndex].hand.pop(twoIndex))
					counterResult.log.append("Player %s makes final counter to resolve the %s with their %s" %(pIndex, card.name(), counterResult.scrap[-1].name()))
					worlds_where_oneOff_resovlves.append(counterResult)

	for game in worlds_where_oneOff_resovlves:
		# Move all points to scrap
		if card.rank == 1 and len(game.players[(pIndex + 1) % 2].points) > 0:
			game.scrap += game.players[0].points
			game.scrap += game.players[1].points
			game.players[0].points = []
			game.players[1].points = []
			game.log.append("Player %s destroys all points with the %s" %(pIndex, card.name()))
			res.append(game)
		# Destroy one face card
		elif card.rank == 2:
			queenCount = game.players[(pIndex + 1) % 2].queenCount()
			if queenCount == 0:
				# Destroy a king or queen
				for index, target in enumerate(game.players[(pIndex + 1) % 2].faceCards):
					twoResult = deepcopy(game)
					twoResult.scrap.append(twoResult.players[(pIndex + 1) % 2].faceCards.pop(index))
					twoResult.log.append("Player %s destroys Player %s's %s with the %s" %(pIndex, (pIndex+1)%2, target.name(), card.name()))
					res.append(twoResult)
				# Destroy a jack to steal point card back
				for index, target in enumerate(game.players[(pIndex + 1) % 2].points):
					if len(target.jacks) > 0:
						twoResult = deepcopy(game)
						twoResult.scrap.append(twoResult.players[(pIndex + 1) % 2].points[index].jacks.pop()) #Move jack to scrap
						twoResult.players[pIndex].points.append(twoResult.players[(pIndex + 1) % 2].points.pop(index)) #Switch control of point card
						twoResult.log.append("Player %s destroys Player %s's %s with the %s and regains control of the %s" %(pIndex, (pIndex+1)%2, twoResult.scrap[-1].name(), card.name(), target.name()))
						res.append(twoResult)
			# If opponent has queen, can only target queen
			elif queenCount == 1:
				twoResult = deepcopy(game)
				for index, target in enumerate(game.players[(pIndex + 1)%2].faceCards):
					if target.rank == 12:
						twoResult.scrap.append(twoResult.players[(pIndex + 1) % 2].faceCards.pop(index))
						twoResult.log.append("Player %s destroys Player %s's %s with the %s" %(pIndex, (pIndex+1)%2, target.name(), card.name()))
				res.append(twoResult)
		elif card.rank == 3:
			for index, target in enumerate(game.scrap):
				threeResult = deepcopy(game)
				threeResult.players[pIndex].hand.append(threeResult.scrap.pop(index))
				threeResult.log.append("Player %s retrieves the %s from the scrap with the %s" %(pIndex, target.name(), card.name()))
				res.append(threeResult)
		# Opponent discards two cards
		elif card.rank == 4 and len(game.players[(pIndex + 1) % 2].hand) > 0:
			game.scrap.append(game.players[(pIndex + 1) % 2].hand.pop())
			if len(game.players[(pIndex + 1) % 2].hand) > 0:
				game.scrap.append(game.players[(pIndex + 1) % 2].hand.pop())
				game.log.append("Player %s makes Player %s discard the %s and %s with the %s" %(pIndex, (pIndex+1)%2, game.scrap[-2].name(), game.scrap[-1].name(), card.name()))
			else:
				game.log.append("Player %s makes Player %s discard the %s with the %s" %(pIndex, (pIndex+1)%2, game.scrap[-1].name(), card.name()))
			res.append(game)
		# Draw 2 cards
		elif card.rank == 5:
			if len(game.deck) > 0:
				# game.scrap.append(game.players[pIndex].hand.pop(cIndex))
				game.players[pIndex].hand.append(game.deck.pop(-1))
				if len(game.deck) > 0:
					game.players[pIndex].hand.append(game.deck.pop(-1))
					game.log.append("Player %s draws two cards with the %s" %(pIndex, card.name()))
				else:
					game.log.append("Player %s draws ONE card with the %s" %s(pIndex, card.name()))
				res.append(game)
		elif card.rank == 6 and len(game.players[(pIndex + 1) % 2].faceCards) > 0:
			game.scrap += game.players[0].faceCards
			game.scrap += game.players[1].faceCards
			game.players[0].faceCards = []
			game.players[1].faceCards = []
			game.log.append("Player %s destroys all face cards with the %s" %(pIndex, card.name()))
			res.append(game)
			pass
		elif card.rank == 7:
			pass
		# Return a card to opponent's hand (they can't play it next turn)
		elif card.rank == 9:
			queenCount = game.players[(pIndex + 1) % 2].queenCount()
			if queenCount == 0:
				for index, target in enumerate(game.players[(pIndex + 1) % 2].faceCards):
					nineResult = deepcopy(game)
					nineResult.players[(pIndex + 1) % 2].hand.append(nineResult.players[(pIndex + 1) % 2].faceCards.pop(index))
					nineResult.players[(pIndex + 1) % 2].hand[-1].frozen = True
					nineResult.log.append("Player %s returns Player %s's %s to her hand with the %s" %(pIndex, (pIndex+1)%2, target.name(), card.name()))
					res.append(nineResult)
				for index, target in enumerate(game.players[(pIndex + 1) % 2].points):
					if target.rank == 10 or (target.rank == 9 and card.suit > target.suit):
						nineResult = deepcopy(game)
						nineResult.players[(pIndex + 1) % 2].hand.append(nineResult.players[(pIndex + 1) % 2].points.pop(index))
						nineResult.players[(pIndex + 1) % 2].hand[-1].frozen = True
						nineResult.log.append("Player %s returns Player %s's %s to her hand with the %s" %(pIndex, (pIndex+1)%2, target.name(), card.name()))
						res.append(nineResult)
					if len(target.jacks) > 0:
						nineResult = deepcopy(game)
						nineResult.players[(pIndex + 1) % 2].hand.append(nineResult.players[(pIndex + 1) % 2].points[index].jacks.pop())
						nineResult.players[pIndex].points.append(nineResult.players[(pIndex + 1) % 2].points.pop(index))
						nineResult.players[(pIndex + 1) % 2].hand[-1].frozen = True
						nineResult.log.append("Player %s returns Player %s's %s to her hand with the %s and regains control of the %s" %(pIndex, (pIndex+1)%2, nineResult.players[pIndex].points[-1].name(), card.name(), target.name()))
						res.append(nineResult)
			elif queenCount == 1:
				nineResult = deepcopy(game)
				for index, target in enumerate(game.players[(pIndex + 1)%2].faceCards):
					if target.rank == 12:
						nineResult.players[(pIndex + 1)%2].hand.append(nineResult.players[(pIndex + 1) % 2].faceCards.pop(index))
						nineResult.players[(pIndex + 1)%2].hand[-1].frozen = True
						nineResult.log.append("Player %s returns Player %s's %s to her hand with the %s" %(pIndex, (pIndex+1)%2, target.name(), card.name()))
				res.append(nineResult)
	return res


# Returns a list of all gamestates resulting from all possible moves
#      that a given player could make this turn
def findPossibleMoves(originalGame, pIndex):
	res =  [] # List of gamestates resulting from possible moves
	game = deepcopy(originalGame) #Copy original game to avoid overwriting it

	# Draw
	if len(game.deck) > 0:
		game.players[pIndex].hand.append(game.deck.pop(-1))	
		game.log.append("Player %s draws" %pIndex)
		res.append(deepcopy(game))
		game = deepcopy(originalGame)

	# Loop through each card in hand and add all legal moves makeable with that card
	for i, card in enumerate(game.players[pIndex].hand):
		if not card.frozen:
			if card.rank < 11:
				# Play points
				game = deepcopy(originalGame)
				name = card.name()
				lenHand = len(game.players[pIndex].hand)
				game.players[pIndex].points.append(game.players[pIndex].hand.pop(i))
				game.log.append("Player %s played the %s for points" %(pIndex, card.name()))
				res.append(deepcopy(game))

				# Scuttle
				# For each opponent's point card, if scuttle is legal, add it to list of possible moves
				for j, pointCard in enumerate(game.players[(pIndex + 1)%2].points):
					if card.rank > pointCard.rank or (card.rank == pointCard.rank and card.suit > pointCard.suit):
						scuttleResult = deepcopy(originalGame)
						scuttleResult.scrap = scuttleResult.scrap + pointCard.jacks #Move jacks to scrap pile
						pointCard.jacks = [] 
						scuttleResult.scrap.append(scuttleResult.players[(pIndex + 1) % 2].points.pop(j)) # Move destroyed point card to scrap
						scuttleResult.scrap.append(scuttleResult.players[pIndex].hand.pop(i)) # Move played card to scrap
						scuttleResult.log.append("Player %s scuttled the %s with the %s" %(pIndex, pointCard.name(), card.name()))
						res.append(deepcopy(scuttleResult))

				# Play as oneOff
				res += playCardAsOneOff(originalGame, pIndex, i)

			# Play king or queen
			elif card.rank > 11:
				game = deepcopy(originalGame)
				game.players[pIndex].faceCards.append(game.players[pIndex].hand.pop(i))
				game.log.append("Player %s played the %s" %(pIndex, card.name()))
				res.append(deepcopy(game))

			# Play jack
			elif card.rank == 11 and game.players[(pIndex + 1) % 2].queenCount() == 0:
				game = deepcopy(originalGame)
				# Loop through all possible jack targets and add move for each one
				for j, pointCard in enumerate(game.players[(pIndex + 1) % 2].points):
					jackResult = deepcopy(originalGame)
					jackResult.players[(pIndex + 1) % 2].points[j].jacks.append(jackResult.players[pIndex].hand.pop(i)) # Move jack from hand to the jacks of targeted point card
					jackResult.players[pIndex].points.append(jackResult.players[(pIndex + 1) % 2].points.pop(j)) # Move stolen point card to this player's points
					jackResult.log.append("Player %s stole the %s with the %s" %(pIndex, pointCard.name(), card.name()))
					res.append(deepcopy(jackResult))

	# Unfreeze all the cards in your hand
	for possibleGame in res:
		for handCard in possibleGame.players[pIndex].hand:
			handCard.frozen = False

	# Separate winning moves, losing moves, and the rest
	win = []
	lose = []
	neither = []
	for game in res:
		if game.winner() == pIndex:
			win.append(game)
		elif game.players[(pIndex + 1) % 2].couldWinNextTurn():
			lose.append(game)
		else:
			neither.append(game)


	if len(win) > 0: # win if possible
		return win
	elif len(neither) > 0: #avoid loss if possible
		return neither
	else: # play losing move if no other options remain
		return lose


def chooseRandomMove(moves):
	return moves[randint(0, len(moves) - 1)]

# Plays two turns of a game (each player plays once)
# Modifies the gameHistory param to append new gamestates
def playRound(gameHistory):
	chosenMove = gameHistory.gameStates[-1] # Gamestate before round
	moves = findPossibleMoves(gameHistory.gameStates[-1], 0)
	stalemate = False
	if len(moves) > 0:
		chosenMove = chooseRandomMove(moves)
		gameHistory.gameStates.append(chosenMove)
	else:
		stalemate = True
	if gameHistory.gameStates[-1].winner() == None:
		moves = findPossibleMoves(chosenMove, 1)
		if len(moves) > 0:
			chosenMove = chooseRandomMove(moves)
			gameHistory.gameStates.append(chosenMove)
		elif stalemate:
			gameHistory.result = "Stalemate"

	return gameHistory

class GamePlayedManyTimes:
	def __init__(self, turnsForGameSeed, numberOfGamesToPlay):
		self.gameSeed = CompleteGame()
		self.resultingGames = []

		# Play turnsForGameSeed many turns
		for i in range(turnsForGameSeed):
			self.gameSeed = playRound(self.gameSeed)

		# Play game to the end numberOfGamesToPlay times
		for i in range(numberOfGamesToPlay):
			self.playGame()

	def playGame(self):
		gameCopy = deepcopy(self.gameSeed)
		while gameCopy.winner() == None and gameCopy.result == None:
			gameCopy = playRound(gameCopy)

		# If not a stalemate, set the winner's index as result
		if gameCopy.result == None:
			gameCopy.result = gameCopy.winner()

		self.resultingGames.append(gameCopy)