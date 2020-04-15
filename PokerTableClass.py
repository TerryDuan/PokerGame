# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 23:33:39 2020

Table class is used to track and drive the game
pot: pot for each game, reset to zero after each game, give pot to winner by player.endGame()
PlayersList: list to store players, [SB, BB, UTG, UTG+1, HJ, CO, BTN], Player at position 0 will be moved to end of list as new BTN

while not end:
    0. Create/Shuffle the deck
    1. check if enough active player, else BREAK
    2. call startGame() on each players in the list, from 0 to END, pass hands and position to each player(agent)
    3. while no winner or before MAX_ITERATION:
        (if street == PreFlop, start from position 2, else start from position 0)
        3a. call player_i.action(), pass through latest updated thisGameActions{}
        3b. update returned tuple into thisGameActions{}
        3c. update table.pot
        3d. if all players checks/called, move to next street, or call find_winner()
        3e. if player is out and inactive, remove it from the playersList
        

@author: terry
"""
from playerClass import Player
from deckClass import Deck

class table():
    
    def __init__(self):
        self.buttomPosition = 0
        self.PlayersList = [] 
        self.pot = 0
        self.bb = 2
        self.sb = 1
        self.MAX_ITERATION = 50

    def addPlayer(self, newPlayer : Player):
        self.PlayersList.append(newPlayer)
        
    def getPot(self):
        return self.pot
    
    def getNPlayer(self):
        return len(self.PlayerList)
    
    def getNPlayer_active(self):
        n = 0
        for plyr in self.PlayersList:
            if plyr[0].isActive():
                n = n + 1
        
        return n
    
    def setBlinds(self, bb : int):
        self.bb = bb
        self.sb = int(bb/2)
        
    def setMaxGames(self, maxGames : int):
        self.MAX_ITERATION = maxGames
    
    def actionValidation(self):
        #check if the returned action is valid
        pass
    
    def runGame(self):
        """
        #main function, start the Game
        #termination condition : hit MAX_ITERATION OR Only one player active
        #create dictionary to keep track of the game        
        thisGameActions : {
                            'Street' : 'PreFlop/Flop/Turn/River',
                            'Actions' : {
                                'PreFLop' : [(playerName:str, action:tuple(str, int)),... etc] ,
                                'Flop' : [] ,
                                'Turn' : [] ,
                                'River' : []
                                },
                            'CommunityCards' : {
                                'Flop' : [Card, Card, Card] ,
                                'Turn' : [] ,
                                'River' : []                                
                                },
                            'Pot' : potSize
                            }
        """
        if self.getNPlayer() < 3:
            print('not enough players')
            return 0

        i = 0 #game id
        #create a deck for following game
        theDeck = Deck(1)        
 
        #Start the 'tournament'
        while True:
            
            if ((i == self.MAX_ITERATION) or (self.getNPlayer_active() < 3)):
                print('All games end')
                return 0
        
            #prepare a new game :
            thisGameAction = {  'Street' : 'PreFlop',
                    'Actions' : {
                        'PreFLop' : [] ,
                        'Flop' : [] ,
                        'Turn' : [] ,
                        'River' : []
                        },
                    'CommunityCards' : {
                        'Flop' : [] ,
                        'Turn' : [] ,
                        'River' : []                                
                        },
                    'Pot' : self.pot,
                    'NPlayers' : len(self.PlayersList)}
            
            print("Game ", " ", i)
            
            
            # Start a new Game, if active, dealt card, give a position, update position
            
            # Shuffle the deck
            theDeck.shuffle(3)
            
            #all players are assumed to be all active
            #dealt card to players, and 'tell them their position in this game'
            for pos, plyr in enumerate(self.PlayersList):
                hand = []
                hand.append(theDeck.dealt())
                hand.append(theDeck.dealt())
                plyr.startGame(hand, pos)
                
            #Game Start:
            #while loop to ask around, move to next street until every one agree on the bet
            for street in ['PreFLop', 'Flop', 'Turn', 'River']:
                
                if street == 'PreFlop':
                    startPosition = 2
                else:
                    startPosition = 0
                    
                """
                TODO: 
                1. PreFlop, force player 0 and player 1 pay SB and BB
                2. Track current max bet, and ask for diff between past bet and max bet
                3. Loop all players, until all players
                    either: a. Fold and isInGame = False
                            b. past bet == max bet
                            c. ALL IN, past bet < max bet and Player's nChip = 0
                4. end this street, move to next, if street == Riever, call findWinner()
                """
                pass
            
            #remove inactive player before next game
            temp = []
            for plyr in self.PlayersList:
                if plyr.isActive() == True:
                    temp.append(plyr)
            self.PlayersList = temp
            
            #change the PlayersList order, move all to right, last to front
            #should we 'move' the seats before remove inactive player?
            temp_player = self.PlayersList.pop()
            self.PlayersList.insert(0, temp_player)
            
            
            #update game id
            i = i + 1
            
        