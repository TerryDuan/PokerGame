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
    SFhead = find_straight_flush(cards)
    Quadhead = find_quad(cards)
    FullHousehead = find_fullhouse(cards)
    Flushhead = find_flush(cards)
    Straighthead = find_straight(cards)
    Sethead = find_set(cards)
    TwoPairs = find_two_pairs(cards)
    Pairhead = find_pair(cards)
    HighCard = find_high_card(cards)
    
    if SFhead != None:
        return "StraightFlush", SFhead
    elif Quadhead != None:
        return "Quad", Quadhead
    elif FullHousehead != None:
        return "FullHouse", FullHousehead
    elif Flushhead != None:
        return "Flush", Flushhead
    elif Straighthead != None:
        return "", Straighthead
    elif Sethead != None:
        return "", Sethead
    elif TwoPairs != None:
        return "", TwoPairs
    elif Pairhead != None:
        return "", Pairhead
    else:
        return "", HighCard

def find_straight(cards):
    PokerCard.cardsRank(cards)
    #hasStraight = False
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
            #hasStraight = True
            return StraightList[0]
        
    return None
        
def find_flush(cards):
    PokerCard.cardsRankBySuitRank(cards)
    FlushList = []
    prevCard = cards[0]
    FlushList.append(prevCard)
    for card in cards[1:]:
        
        #check if current one is next to prevCard
        if prevCard == card:
            FlushList.append(card)
        else:
            FlushList = []
            FlushList.append(card)
        
        prevCard = card
        
        if len(FlushList) == 5:
            #found the Set
            return FlushList[0]

    return None

def find_straight_flush(cards):
    PokerCard.cardsRankBySuitRank(cards)
    SFList = []
    prevCard = cards[0]
    SFList.append(prevCard)
    for card in cards[1:]:
        
        #check if current one is next to prevCard
        if ((prevCard == card) and (prevCard - card == 1)):
            SFList.append(card)
        else:
            SFList = []
            SFList.append(card)
        
        prevCard = card
        
        if len(SFList) == 5:
            #found the Set
            return SFList[0]

    return None

def find_quad(cards):
    PokerCard.cardsRank(cards)
    QuadList = []
    prevCard = cards[0]
    QuadList.append(prevCard)
    for card in cards[1:]:
        
        #check if current one is next to prevCard
        if prevCard - card != 0:
            QuadList = []
            QuadList.append(card)
        else:
            QuadList.append(card)
        
        prevCard = card
        
        if len(QuadList) == 4:
            #found the Set
            return QuadList[0]

    return None

def find_fullhouse(cards):
    setHead = find_set(cards)
    pairsHead = find_two_pairs(cards)
    
    if len(pairsHead) > 0 and setHead != None:
        for card in pairsHead:
            if card - setHead != 0:
                return setHead
        
    return None
    

def find_set(cards):
    PokerCard.cardsRank(cards)
    SetList = []
    prevCard = cards[0]
    SetList.append(prevCard)
    for card in cards[1:]:
        
        #check if current one is next to prevCard
        if prevCard - card != 0:
            SetList = []
            SetList.append(card)
        else:
            SetList.append(card)
        
        prevCard = card
        
        if len(SetList) == 3:
            #found the Set
            return SetList[0]

    return None

def find_pair(cards):
    PokerCard.cardsRank(cards)
    
    try:
        prevCard = cards[0]
    except:
        return None
    
    
    for card in cards[1:]:

        #check if current one is next to prevCard
        if prevCard - card == 0:
            return prevCard
        else:
            prevCard = card
        
    return None

def find_two_pairs(cards):
    PokerCard.cardsRank(cards)
    
    try:
        prevCard = cards[0]
    except:
        return None
    
    pairsHeads = []
    index = 1
    
    if len(cards) > 1:
        while index < len(cards):
            if prevCard - cards[index] == 0:
                pairsHeads.append(prevCard)
                
                if index + 1 == len(cards):
                    break#early stop, TODO: overwrite the loop to do while loop.
                
                prevCard = cards[index + 1]
                index = index + 2
            else:
                prevCard = cards[index]
                index = index + 1
            
        
    return pairsHeads

def find_high_card(cards):
    PokerCard.cardsRank(cards)
    try:
        return cards[0]
    except:
        print("No Cards in the List")
        return None

def find_winner(**args):
    """
    given multiple players hands, and community cards, determin the winner
    """
    pass