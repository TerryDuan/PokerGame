# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 22:41:44 2020

@author: terry

Player class to 
-track each player's chips 
-store playes's hand on each round
-return decition from action() when called upon

Child classes will implement different action()

"""
import TexasHoldemCalculators_v0 as calc 
from cardClass import Card, PokerCard

class Player():
    
    def __init__(self, nChip : int):
        
        self.nChip = nChip
        
        self.hand = [] # do we need make a copy of cards from desk class
        self.position = None
        self.active = False
    

    def isActive(self):

        return self.acitve            
        
    def startGame(self, yourHand : list, yourPosition : int):
        """
        Called once every game
        """
        self.acitve  = True
        self.hand = yourHand
        self.position = yourPosition
        
    def endGame(self, payoff : int):
        """
        Called once every game, by Table or After 'FOLD' action
        """
        self.active = False
        self.hand = []
        self.position = None
     
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
        
        