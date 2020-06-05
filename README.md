# PokerGame

This is a Python library to simulate a No Limit Texas Hold'em Game.
Under current version,  the Game is simplified as No Straddle No Re-entry Game.

## Installation


## Usage
### Example

```python
from playerClass import Player
from smarterPlayer import smarterPlayer
from interactivePlayer import interactivePlayer
from PokerTableClass import table

#create 5 dummy player, 1 smarterPlayer
p1 = Player("p1")
p2 = Player("p2")
p3 = Player("p3")
p4 = Player("p4")
p5 = Player("p5")
p6 = smarterPlayer("sp6")

#create table
aTable = table()
aTable.setMaxGames(1000)

#adding players
aTable.addPlayer(p1,100)
aTable.addPlayer(p2,100)
aTable.addPlayer(p3,100)
aTable.addPlayer(p4,100)
aTable.addPlayer(p5,100)
aTable.addPlayer(p6,100)

print("Table Setted up with Six dummy player")
print("Number of Players " + str(aTable.getNPlayer()))
print("Number of Active Players " + str(aTable.getNPlayer_active()))
print("Number of inGame Players " + str(aTable.getNPlayer_inGame()))

#run the game
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

User can play with the bots through the interactive Player agent.
User need to Type in Action and Bet Size

#### Example:

```python
p5 = interactivePlayer("ip5")
```

```python
***************************
current street  PreFlop  your position  4
your hand  h9 s9
your stack  100
bet to call  2.0
community cards 
current Street Bet History
{'PreFlop': [1, 2, 2.0, 2.0, nan, nan], 'Flop': [nan, nan, nan, nan, nan, nan], 'Turn': [nan, nan, nan, nan, nan, nan], 'River': [nan, nan, nan, nan, nan, nan]}

type in your action: BET

type in your bet (int): 100

***************************
```
### GUI

Under Development :)

### Simulation History

After the simulation, the history for each game will be saved as pickle file in the GameHistory folder.
A log file will also be created for debugging purpose.

## Contributing

Pull requests are welcome.
For major changes, or bugs, please open an issue or directly contact me at:
terry.w.duan@gmail.com

## License