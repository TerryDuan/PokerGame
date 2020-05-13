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
        return 1, SFhead
    elif Quadhead != None:
        return 2, Quadhead
    elif FullHousehead != None:
        return 3, FullHousehead
    elif Flushhead != None:
        return 4, Flushhead
    elif Straighthead != None:
        return 5, Straighthead
    elif Sethead != None:
        return 6, Sethead
    elif TwoPairs != None:
        return 7, TwoPairs
    elif Pairhead != None:
        return 8, Pairhead
    else:
        return 9, HighCard

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
            return StraightList
        
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
            return FlushList

    return None

def find_straight_flush(cards):
    """
    Find Straight Flush

    Parameters
    ----------
    cards : TYPE
        DESCRIPTION.

    Returns
    -------
    SFList : TYPE
        DESCRIPTION.

    """
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
            return SFList

    return None

def find_quad(cards):
    """
    Find best quads + one high card

    Parameters
    ----------
    cards : TYPE
        DESCRIPTION.

    Returns
    -------
    QuadList : TYPE
        DESCRIPTION.

    """
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
            break
        
    if len(QuadList) == 4:
        for card in cards:
            if card - QuadList[0] != 0:
                QuadList.append(card)
                return QuadList
    else:
        return None

def find_fullhouse(cards):
    setHead = find_set(cards)
    pairsHead = find_two_pairs(cards)
    fullhouseList = []    
    
    if len(pairsHead) > 0 and len(setHead) > 0:
        fullhouseList = setHead[0:3]
        for card in pairsHead:
            if card - setHead[0] != 0:
                fullhouseList.append(card)
            
            if len(fullhouseList) == 5:
                return fullhouseList
    
        
    return None
    

def find_set(cards):
    """
    Find best three cards with same rank + two highest ranked cards

    Parameters
    ----------
    cards : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    PokerCard.cardsRank(cards)
    SetList = []
    
    try:
        prevCard = cards[0]
    except:
        return None
    
    SetList.append(prevCard)
    
    for card in cards[1:]:

        #check if current one is next to prevCard
        if prevCard - card == 0:
            SetList.append(card)
        else:
            SetList = []
            SetList.append(card)
        
        prevCard = card
        
        if len(SetList) == 3:
            break
        
        
    if len(SetList) == 3:
        for card in cards:
            if card - SetList[0] != 0:
                SetList.append(card)
                
            if len(SetList) == 5:
                return SetList
            
        return None
    else:
        return None

def find_pair(cards):
    """
    Find best pair of cards + three highest ranked cards

    Parameters
    ----------
    cards : TYPE
        DESCRIPTION.

    Returns
    -------
    prevCard : TYPE
        DESCRIPTION.

    """
    PokerCard.cardsRank(cards)
    PairsList = []
    
    try:
        prevCard = cards[0]
    except:
        return None
    
    PairsList.append(prevCard)
    
    for card in cards[1:]:

        #check if current one is next to prevCard
        if prevCard - card == 0:
            PairsList.append(card)
            break
        else:
            PairsList = []
            PairsList.append(card)
        
        prevCard = card
        
    if len(PairsList) == 2:
        for card in cards:
            if card - PairsList[0] != 0:
                PairsList.append(card)
                
            if len(PairsList) == 5:
                return PairsList
            
        return None
    else:
        return None

def find_two_pairs(cards):
    """
    Find best two pairs + one highest ranked cards

    Parameters
    ----------
    cards : TYPE
        DESCRIPTION.

    Returns
    -------
    pairsHeads : TYPE
        DESCRIPTION.

    """
    PokerCard.cardsRank(cards)
    PairsList = []
    
    try:
        prevCard = cards[0]
    except:
        return None
    
    PairsList.append(prevCard)
    
    for card in cards[1:]:

        #check if current one is next to prevCard
        if prevCard - card == 0:
            PairsList.append(card)
            break
        else:
            PairsList = []
            PairsList.append(card)
        
        prevCard = card
    
    AnotherPairs = []    
    if len(PairsList) == 2:
        prevCard = cards[0]
        for card in cards[1:]:
            if ((prevCard - card == 0)&(card - PairsList[0] != 0)):
                AnotherPairs.append(prevCard)
                AnotherPairs.append(card)
                break
            else:
                prevCard = card
        
    TwoPairs = []
    TwoPairs = TwoPairs + PairsList + AnotherPairs
    
    if len(TwoPairs) == 4:
        for card in cards:
            if ((card - PairsList[0] != 0)&(card - AnotherPairs[0] != 0)):
                TwoPairs.append(card)
                break
        
        return TwoPairs
    else:
        return None

def find_high_card(cards):
    PokerCard.cardsRank(cards)
    try:
        return cards[0:5]
    except:
        print("No Cards in the List")
        return None

def find_winner(community_cards , player_hands):
    """
    Combine community_cards with each player's hand, compare ComboRank
    
    Parameters
    ----------
    community_cards : List
        List of five cards.
    player_hands : Dict
        key : player's index,
        value : list of two cards

    Returns
    -------
    list of winner(s)

    """
    results = []
    for key in player_hands:
        cards = community_cards + player_hands[key]
        ComboRank, Combo = find_best_combo(cards)
        results.append((key, ComboRank, Combo))
    
    results.sort(key = lambda x: x[1])
    all_winners = [] #for multiple users
    
    if len(results) == 1:
        return [results[0][0]]
    else:
        bestResult = results[0]
        all_winners.append(bestResult)
        for result in results[1:]:
            
            if bestResult[1] != result[1]:
                break
            else:
                all_winners.append(result)
                
            bestResult = result
                
    if len(all_winners) == 1:
        return [all_winners[0][0]]
    else:
        for result in all_winners:
            #TODO: diff senararios based on combe
            pass
    
    
        