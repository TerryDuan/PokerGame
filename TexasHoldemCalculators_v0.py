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
    
    if len(SFhead) != 0:
        return 1, SFhead
    elif len(Quadhead) != 0:
        return 2, Quadhead
    elif len(FullHousehead) != 0:
        return 3, FullHousehead
    elif len(Flushhead) != 0:
        return 4, Flushhead
    elif len(Straighthead) != 0:
        return 5, Straighthead
    elif len(Sethead) != 0:
        return 6, Sethead
    elif len(TwoPairs) != 0:
        return 7, TwoPairs
    elif len(Pairhead) != 0:
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
        
    return []
        
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

    return []

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

    return []

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
        return []

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
    
        
    return []
    

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
        return []
    
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
            
        return []
    else:
        return []

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
        return []
    
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
            
        return []
    else:
        return []

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
        return []
    
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
        return []

def find_high_card(cards):
    PokerCard.cardsRank(cards)
    try:
        return cards[0:5]
    except:
        print("No Cards in the List")
        return []

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
        all_winners.append(results[0])
        return _prepare_winner_index_list(all_winners)
    else:
        bestResult = results[0]
        all_winners.append(bestResult)
        for result in results[1:]:
            
            if bestResult[1] != result[1]:
                return all_winners
            else:
                all_winners.append(result)
                
            bestResult = result
                
    if len(all_winners) == 1:
        return _prepare_winner_index_list(all_winners) #one winner
    else:
        final_winner_list = []
        
        maxWinner = all_winners[0]
        for result in all_winners[1:]:
            #TODO: diff senararios based on combe
            #print(maxWinner, result)
            prevVScurrent = _compareTwoCombo(maxWinner[2], result[2])
            
            if prevVScurrent == -1:
                maxWinner = result
                
        for result in all_winners:
            
            prevVScurrent = _compareTwoCombo(maxWinner[2], result[2])
            if ((prevVScurrent != 1) and (prevVScurrent != -1)):
                final_winner_list.append(result[0])
                
        
        return final_winner_list
                

def _prepare_winner_index_list(all_winners):
    final_list = []
    for winner in all_winners:
        final_list.append(winner[0])
    return final_list

def _compareTwoCombo(combo1, combo2):
    if ((len(combo1) != len(combo2)) or (len(combo1) == 0) or (len(combo2) == 0)):
        return None
    else:
        i = 0
        while i < len(combo1):
            
            if combo1[i] - combo2[i] > 0:
                return 1
            elif combo1[i] - combo2[i] < 0:
                return -1
            else:
                i = i + 1
        
        return 0
    
        