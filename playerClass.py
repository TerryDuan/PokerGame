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
import TexasHoldemCalculators as calc 
from cardClass import Card, PokerCard

class Player():
    
    def __init__(self, name : str):
        
        self.name = name
        
        self.hand = [] # do we need make a copy of cards from desk class
        self.position = None
        self.active = True
        self.inGame = False
    
    def name(self):
        return self.name
    

    def isActive(self):

        return ((self.active))   

    def isInGame(self):
        
        return self.inGame         
        
    def startGame(self, yourHand : list, yourPosition : int):
        """
        Called once every game, by Table
        If Straddle is allowed, need to override this method
        """
        #self.acitve  = True 
        self.inGame = True
        self.hand = yourHand
        self.position = yourPosition
        
            
        
    def endGame(self):
        """
        Called once every game, by Table, After 'FOLD' action or After River
        """
        #self.active = False
        self.inGame = False
        self.hand = []
        self.position = None
        
    def _getCurrentStack(self, thisGameActions : dict):
        """
        Based on thisGameActions, get current stacks
        return number of Chips
        """
        try:
            result = thisGameActions['PlayerStack'][thisGameActions['PublicPlayersList'].index(self.name)]
            return result
        except:
            return -1
        
     
    def action(self, chipsToCall : int, thisGameActions : dict):
        """
        Dummy Player for testing purpose
        
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
        
        nChip = self._getCurrentStack(thisGameActions)
        
        if self.position < 2:
            
            return 'CALL' , chipsToCall
        elif chipsToCall < nChip:
            
            return 'CALL', chipsToCall
        else:
            self.endGame()
            return 'FOLD' , 0
        
        