from game import Game
from copy import deepcopy
import pickle

def findPossibleMoves(originalGame, pIndex):
	res =  [originalGame]
	game = deepcopy(originalGame)
	# player = game.players[pIndex]

	# Draw
	if len(game.deck) > 0:
		game.players[pIndex].hand.append(game.deck.pop(-1))	
		res.append(deepcopy(game))
		game = deepcopy(originalGame)

	# Play to field
	for i, card in enumerate(game.players[pIndex].hand):
		if card.rank < 11:
			game = deepcopy(originalGame)
			name = card.name()
			lenHand = len(game.players[pIndex].hand)
			game.players[pIndex].points.append(game.players[pIndex].hand.pop(i))
			game.print()
			res.append(deepcopy(game))
		elif card.rank > 11:
			game = deepcopy(originalGame)
			game.players[pIndex].faceCards.append(game.players[pIndex].hand.pop(i))
			res.append(deepcopy(game))

	return res

firstGame = Game()
print("First game:")
firstGame.print()
moves = findPossibleMoves(firstGame, 0)
print("\ngot %s moves" %len(moves))
print("Possible moves:\n")
for i, move in enumerate(moves):
	print("\nGame %s" %i)
	move.print()


# Store results on disk
# with open('./game.pkl', 'rb') as f:
# 	gameList = pickle.load(f)
# 	gameList.append(firstGame)
# 	for game in gameList:
# 		game.print()

# with open('./game.pkl', 'wb') as f:
# 	pickle.dump(gameList, f)
