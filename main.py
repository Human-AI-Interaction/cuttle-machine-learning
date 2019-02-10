from copy import deepcopy
from random import randint
import pickle
from game import Game
from completegame import CompleteGame

def findPossibleMoves(originalGame, pIndex):
	res =  [originalGame]
	game = deepcopy(originalGame)
	# player = game.players[pIndex]

	# Draw
	if len(game.deck) > 0:
		game.players[pIndex].hand.append(game.deck.pop(-1))	
		res.append(deepcopy(game))
		game = deepcopy(originalGame)

	# Loop through each card in hand and add all legal moves makable with that card
	for i, card in enumerate(game.players[pIndex].hand):
		if card.rank < 11:
			# Play to field
			game = deepcopy(originalGame)
			name = card.name()
			lenHand = len(game.players[pIndex].hand)
			game.players[pIndex].points.append(game.players[pIndex].hand.pop(i))
			# game.print()
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
					res.append(deepcopy(scuttleResult))

		# Play king or queen
		elif card.rank > 11:
			game = deepcopy(originalGame)
			game.players[pIndex].faceCards.append(game.players[pIndex].hand.pop(i))
			res.append(deepcopy(game))

		elif card.rank == 11 and game.players[(pIndex + 1) % 2].queenCount() == 0:
			game = deepcopy(originalGame)
			for j, pointCard in enumerate(game.players[(pIndex + 1) % 2].points):
				jackResult = deepcopy(originalGame)
				jackResult.players[(pIndex + 1) % 2].points[j].jacks.append(jackResult.players[pIndex].hand.pop(i)) # Move jack from hand to the jacks of targeted point card
				jackResult.players[pIndex].points.append(jackResult.players[(pIndex + 1) % 2].points.pop(j)) # Move stolen point card to this player's points
				res.append(deepcopy(jackResult))

	return res



def chooseRandomMove(moves):
	return moves[randint(0, len(moves) - 1)]

def playRound(gameHistory):
	moves = findPossibleMoves(gameHistory.gameStates[-1], 0)
	chosenMove = chooseRandomMove(moves)
	gameHistory.gameStates.append(chosenMove)



	if gameHistory.gameStates[-1].winner() == None:
		moves = findPossibleMoves(chosenMove, 1)
		chosenMove = chooseRandomMove(moves)
		gameHistory.gameStates.append(chosenMove)

	if gameHistory.gameStates[-1].winner() != None:
		print("\n\nWINNER: %s" %gameHistory.gameStates[-1].winner())
	return gameHistory


gameHistory = CompleteGame() # Class to stor list of game states until win or stalemate
gameHistory.gameStates.append(Game()) # Create initial game at beginning of list

# playRound(gameHistory)
# gameHistory.gameStates[-1].print()
# playRound(gameHistory)
# gameHistory.gameStates[-1].print()
# playRound(gameHistory)
# gameHistory.gameStates[-1].print()
# playRound(gameHistory)
# gameHistory.gameStates[-1].print()

# Play until there is a winner
while gameHistory.gameStates[-1].winner() == None:
	playRound(gameHistory)
# Print game history
gameHistory.print()

# moves = findPossibleMoves(firstGame, 0)
# print("\ngot %s moves" %len(moves))
# print("Possible moves:\n")
# for i, move in enumerate(moves):
# 	print("\nGame %s" %i)
# 	move.print()


# Store results on disk
# with open('./game.pkl', 'rb') as f:
# 	gameList = pickle.load(f)
# 	gameList.append(firstGame)
# 	for game in gameList:
# 		game.print()

# with open('./game.pkl', 'wb') as f:
# 	pickle.dump(gameList, f)
