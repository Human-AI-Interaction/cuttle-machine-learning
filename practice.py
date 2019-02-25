from gameplayedmanytimes import GamePlayedManyTimes
from timeit import default_timer as timer

start = timer()

x = 2
y = 20
data = GamePlayedManyTimes(x, y)


data.resultingGames[-1].print()

for game in data.resultingGames:
	print("\n\nPossible game:")
	game.print()

print("\nResults:")
for game in data.resultingGames:
	print("winner: %s " %(game.winner()))

end = timer()
print("Ran turn %s gameseed %s times in %ss" %(x, y, end-start))