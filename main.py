from copy import deepcopy
from random import randint
import pickle
from game import Game
from completegame import CompleteGame

# Returns the result of playing a given card as a oneOff
	# Returns array of possible results (in case card can be played multiple ways)
def playCardAsOneOff(originalGame, pIndex, cIndex):
	res = []
	game = deepcopy(originalGame)
	card = game.players[pIndex].hand[cIndex]
	# Move all points to scrap
	if card.rank == 1:
		game.scrap += game.players[0].points
		game.scrap += game.players[1].points
		game.players[0].points = []
		game.players[1].points = []
		game.log.append("Player %s destroys all points with the %s" %(pIndex, card.name()))
		res.append(game)
	elif card.rank == 2:
		pass
	elif card.rank == 3:
		pass
	elif card.rank == 4:
		pass
	elif card.rank == 5:
		pass
	elif card.rank == 6:
		game.scrap += game.players[0].faceCards
		game.scrap += game.players[1].faceCards
		game.players[0].faceCards = []
		game.players[1].faceCards = []
		game.log.append("Player %s destroys all face cards with the %s" %(pIndex, card.name()))
		res.append(game)
		pass
	elif card.rank == 7:
		pass
	elif card.rank == 9:
		pass
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

	return res


def chooseRandomMove(moves):
	return moves[randint(0, len(moves) - 1)]

# Plays two turns of a game (each player plays once)
# Modifies the gameHistory param to append new gamestates
def playRound(gameHistory):
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

# Play full game until there is a winner
# Returns complete game object with full game history
def playGame():
	gameHistory = CompleteGame()
	# Play until there is a winner or staelemate
	while gameHistory.winner() == None and gameHistory.result == None:
		playRound(gameHistory)
	# If no stalemate, set the result to index of winner
	if gameHistory.result == None:
		gameHistory.result = gameHistory.winner()
	return gameHistory

# Plays n games and returns list of CompleteGames
def playNGames(n):
	res = []
	for i in range(n):
		res.append(playGame())
	return res




gameList = []

##############################
# Loading and saving results #
##############################
# Read old list of complete games
with open('./game.pkl', 'rb') as f:
	gameList = pickle.load(f)

# Add new games 
gameList += playNGames(1) #This param sets how many games are added to list
print("Saved a total of %s games" %len(gameList))
for game in gameList:
	print("\n\n===================================================")
	game.print()

# Save results to disk
with open('./game.pkl', 'wb') as f:
	pickle.dump(gameList, f)
