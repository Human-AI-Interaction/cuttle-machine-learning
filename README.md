# Machine Learning with Cuttle Bot!

This project is intended to improve the decision making of an Educational AI that plays the card game [Cuttle](https://www.pagat.com/combat/cuttle.html)

It crates data representing full games of cuttle where both players made random legal moves until there is a winner or stalemate.

This data will be analyzed with a weight-based model (re-enforcement learning) to produce an evaluator function that can read the intermediate state of a game to calculate the probability of it resulting in a win for either player. This will eventually be incorporated into the MiniMax algorithm of [CuttleBot](https://human-ai-interaction.github.io/cuttle-bot/)

# Organization
Class files are stored in card.py, player.py, game.py (representing a snapshot of a game), and completegame.py (representing the full sequence of gamestates at every turn of a game, through completion).

main.py defines and executes the functions that play games 

# Data Structure
### Card
A Card has a suit and rank, as well as a list of jacks that are currently attached to it (jacks steal a card)

### Player
A Player has a hand, points, and faceCards, three separate lists of cards, as well as helper methods for counting relevant attributes and printing the current state of the player

### Game
Represents a snapshot of a game. Has a deck and scrap (lists of cards), and players (list of two players), along with helper methods for printing and identifying a winner.

### CompleteGame
Represents every turn of a game, from beginning to end. Has gameStates (a list of games, each representing the result of one turn).