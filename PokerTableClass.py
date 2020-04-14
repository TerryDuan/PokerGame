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
    3. while no winner:
        (if street == PreFlop, start from position 2, else start from position 0)
        3a. call player_i.action(), pass through latest updated thisGameActions{}
        3b. update returned tuple into thisGameActions{}
        3c. update table.pot
        3d. if all players checks/called
        

@author: terry
"""
from playerClass import Player
from deckClass import Deck

class table():
    
    def __init__(self):
        self.buttomPosition = 0
        self.PlayersList = [] #can it contains both parent class and child class?
        self.pot = 0
        self.bb = 2
        self.sb = 1
        self._tempPosition = 0
        self.MAX_ITERATION = 50

    def addPlayer(self, newPlayer : Player):
        self.PlayerList.append((newPlayer, self._tempPosition))
        self._tempPosition = self._tempPosition + 1
        
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
                            'Pot' : self.pot}
        
        UTG_table_position = -1
        BB_table_position = 0
        BTN__table_position = 2
        i = 0
        
        while True:
            
            print("Game ", " ", i)
            
            if ((i == self.MAX_ITERATION) or (self.getNPlayer_active() < 3)):
                print('All games end')
                return 0
            
            for plyr in self.PlayersList:
                plyr[0].
                plyr[1]
            
            
            i = i + 1
            
        