# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 22:21:46 2020

@author: terry
"""
from cardGraph import cardPic

class Card:
    
    SUITFACE = {'h':'♥',
                's':'♠',
                'c':'♣',
                'd':'♦'}
    
    def __init__(self, rank : str, suit : str):
        self.rank = rank.upper()
        self.suit = suit.lower()
        
    def __str__(self):
        return str(self.suit) + str(self.rank)

    def __eq__(self, other):
        return ((self.rank == other.rank) & (self.suit == other.suit))
    
    def getValue(self):
        #return a tuple with rank and suit(letter)
        return self.suit, self.rank
    
    def prettyCard(self):
        
        return cardPic[self.rank].format(self.SUITFACE[self.suit])
        
class PokerCard(Card):
    
    """
    # Define special orders for Poker (Texas Holdem, Omaha etc.)
    # Define special comparison logic for cards in Poker games
    # Define sort for cards in Poker games
    """
    
    
    CARDRANK = {
        '2': 1,
        '3': 2,
        '4': 3,
        '5': 4,
        '6': 5,
        '7': 6,
        '8': 7,
        '9': 8,
        '10': 9,
        'J': 10,
        'Q': 11,
        'K': 12,
        '1': 13
        }
    
    #overwrite == : TRUE IF suited
    def __eq__(self, other):
        return ((self.suit == other.suit))
    
    #overwrite != : TRUE IF not suited and not equal rank
    def __ne__(self, other):
        return ((self.rank != other.rank) & (self.suit != other.suit))
    
    # (__eq__ == False and __ne__ == False) IF pairs
    
    #overwrite < : TRUE IF rank is less, and not suited
    def __lt__(self, other):
        return((self.CARDRANK[self.rank] < self.CARDRANK[other.rank]) & (self.suit != other.suit))
    
    #overwrite <= : TRUE IF rank is less, and suited
    def __le__(self, other):
        return((self.CARDRANK[self.rank] < self.CARDRANK[other.rank]) & (self.suit == other.suit))
    
    #overwrite > : TRUE IF rank is larger, and not suited
    def __gt__(self, other):
        return((self.CARDRANK[self.rank] > self.CARDRANK[other.rank]) & (self.suit != other.suit))
    
    #overwrite >= : TRUE IF rank is larger, and suited
    def __ge__(self, other):
        return((self.CARDRANK[self.rank] > self.CARDRANK[other.rank]) & (self.suit == other.suit))
    
    #overload + and -
    def __sub__(self, other):
        return self.CARDRANK[self.rank] - self.CARDRANK[other.rank]
    
    def __add__(self, other):
        return self.CARDRANK[self.rank] + self.CARDRANK[other.rank]
    
    #@staticmethod
    #this will force you to use PokerCard.CARDRANK
    #, which will be a problem for other games （other child class)
    @classmethod
    def cardsRank(cls, cards : list):
        cards.sort(key = lambda x: cls.CARDRANK[x.rank], reverse = True)
        
    @classmethod
    def cardsRankBySuitRank(cls, cards : list):
        cards.sort(key = lambda x: [x.suit,cls.CARDRANK[x.rank]], reverse = True)
