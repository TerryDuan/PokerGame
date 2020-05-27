# PokerGame

This is a Python library to simulate a No Limit Texas Hold'em Game.
Under current version,  the Game is simplified as No Straddle No Re-entry Game.

## Installation


## Usage
### Example

```python
from playerClass import Player
from PokerTableClass import table

#create dummy player
p1 = Player(100, "p1")
p2 = Player(100, "p2")
p3 = Player(100, "p3")
p4 = Player(100, "p4")
p5 = Player(100, "p5")
p6 = Player(100, "p6")

#create a table, and set max number of games
aTable = table()
aTable.setMaxGames(1000)

#add players to table
aTable.addPlayer(p1)
aTable.addPlayer(p2)
aTable.addPlayer(p3)
aTable.addPlayer(p4)
aTable.addPlayer(p5)
aTable.addPlayer(p6)

#start the game
aTable.runGame()
```

### Create User Defined Player with smarter strategy
#### User can create child class from Player class to re-define the action() method
Parameters | Description
---------- | -----------
chipsToCall | number of chips the player need to return to keep playing (e.g. 2 to call previous bet)
thisGameActions | a dictionary with all the past actions/bets/decisions for current game

Returns    | Description
---------- | -----------
action | a string for the type of actions (valid actions: ALL IN, BET，RAISE, CALL, CHECK, FOLD)
chipsToCall | number of chips pay to the table/pot

### Create an interactive Player agent

TODO

### Simulation History

After the simulation, the history for each game will be saved as pickle file in the GameHistory folder.
A log file will also be created for debugging purpose.

## Contributing

Pull requests are welcome.
For major changes, or bugs, please open an issue or directly contact me at:
terry.w.duan@gmail.com

## License