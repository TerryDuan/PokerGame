# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 19:31:04 2020

@author: terry
"""


from cardClass import Card, PokerCard
import random


class Deck():    
    
    def __init__(self, nDecks : int, typ = 'poker'):
        
        self.nDecks = nDecks
        
        if typ == 'poker':
            self.CardType = PokerCard
        else:
            self.CardType = Card
            
        self.newDeck = self._createFullDeck()*nDecks

    #define a list of cards in a full deck, without jokers
    def _createFullDeck(self):
        
        aDeck = []
        ranks = [str(i) for i in range(1,11)] + ['J', 'Q', 'K']
        suits = ['s','c','h','d']
        
        for suit in suits:
            for rank in ranks:
                aDeck.append(self.CardType(rank, suit))
        
        return aDeck
    
    def getValue(self):
        return self.newDeck
    
    def printDeck(self):
        for card in self.newDeck:
            print(card.getValue())
            
    def printPrettyDeck(self):
        for card in self.newDeck:
            print(card.prettyCard())
            
    def shuffle(self, seed : int):
        
        # check if missing card, rebuild the deck if missing
        if self._checkIfCardMissing():
            print('card missing, need reCreate the Deck')
            self.newDeck = self._createFullDeck()*nDecks
        
        random.seed(seed)
        random.shuffle(self.newDeck)
            
    def dealt(self):
        pass
        #pop one
        #add it back to end
        self.newDeck.insert(0, self.newDeck.pop())        
        #return a card/pokerCard
        return self.newDeck[0]
        
    def _checkIfCardMissing(self):
        return len(self.newDeck) != 52*self.nDecks

