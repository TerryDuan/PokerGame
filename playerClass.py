# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 22:41:44 2020

@author: terry

Player class to 
-track each player's chips 
-store playes's hand on each round
-return decition from action() when called upon
-active: initially True, if the player choose to exit or the nChip below 1, then False
-isActive() will be called by Table to check if the player will be included before dealing the card
-inGame, to track if player already foled in each game, reset when startGame()

Child classes will implement different action()
Child classes will with option to rebuy() and change active to True before return FOLD

"""
import TexasHoldemCalculators_v0 as calc 
from cardClass import Card, PokerCard

class Player():
    
    def __init__(self, nChip : int, name : str):
        
        self.name = name
        self.nChip = nChip
        
        self.hand = [] # do we need make a copy of cards from desk class
        self.position = None
        self.active = True
        self.inGame = False
    
    def name(self):
        return self.name

    def isActive(self):

        return ((self.acitve) and (self.nChip >= 1))   

    def isInGame(self):
        
        return self.inGame         
        
    def startGame(self, yourHand : list, yourPosition : int, cost2Start = 0):
        """
        Called once every game
        """
        #self.acitve  = True
        self.inGame = True
        self.hand = yourHand
        self.position = yourPosition
        
        if yourPosition <= 1:
            if self.nChip < cost2Start:
                chip = self.nChip
                self.nChip = 0
                return chip
            else:
                return cost2Start
        else:
            return 0
            
        
    def endGame(self, payoff : int):
        """
        Called once every game, by Table or After 'FOLD' action
        """
        #self.active = False
        self.inGame = False
        self.hand = []
        self.position = None
        
        #check if the player has enough chip for next game
        if self.nChip < 1:
            self.active = False
     
    def action(self, chipsToCall : int, thisGameActions : dict):
        """
        chipsToCall : number of chips need to pay to call, >= 0
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
        
        
        if self.position < 2:
            #currently big or small blind
            #pay the blinds, and call any bet
            self.nChip = self.nChip + self.position - chipsToCall
            return 'CALL' , chipsToCall
        else:
            self.endGame(0)
            return 'FOLD' , 0
        
        