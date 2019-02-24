from gameplayedmanytimes import GamePlayedManyTimes

x = 2
y = 5
data = GamePlayedManyTimes(x, y)

print("Ran turn %s gameseed %s times" %(x, y))
data.resultingGames[-1].print()

for game in data.resultingGames:
	print("\n\nPossible game:")
	game.print()

print("\nResults:")
for game in data.resultingGames:
	print("winner: %s " %(game.winner()))