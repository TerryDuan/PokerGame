# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 22:32:33 2020

@author: terry

helper functions for playerClass's action()
"""
from cardClass import Card, PokerCard

def calc_prob(c1 : PokerCard, c2 : PokerCard):
    pass

def calc_equity():
    pass

def find_best_combo(cards):
    """
    Given 7 cards, select 5 to form the best combo

    Parameters
    ----------
    cards : TYPE
        DESCRIPTION.

    Returns
    -------
    str: combo_code

    """
    pass

def find_straight(cards):
    PokerCard.cardsRank(cards)
    hasStraight = False
    StraightList = []
    prevCard = cards[0]
    StraightList.append(prevCard)
    for card in cards[1:]:

        #check if current one is next to prevCard
        if prevCard - card > 1:
            # current one is more than 2 notch less, straight is broken
            StraightList = []
            StraightList.append(card)
        elif prevCard - card == 1:
            StraightList.append(card)
        else:
            #same rank, skip
            pass
        
        prevCard = card
        
        if len(StraightList) == 5:
            #found the fifth one
            hasStraight = True
            return str(StraightList[0])
        
    return "No Straight"
        

def find_winner(**args):
    """
    given multiple players hands, and community cards, determin the winner
    """
    pass