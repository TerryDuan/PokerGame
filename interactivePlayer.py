# -*- coding: utf-8 -*-
"""
Created on Wed May 27 22:47:40 2020

@author: terry
"""


from playerClass import Player
import TexasHoldemCalculators as calc

class interactivePlayer(Player):
    
    
    def action(self, chipsToCall : int, thisGameActions : dict):
        """
        Position based strategy, Fixed range
        """
        
        nChip = self._getCurrentStack(thisGameActions)
        community_card = []
        community_card = thisGameActions['CommunityCards']['Flop'] + thisGameActions['CommunityCards']['Turn'] + thisGameActions['CommunityCards']['River']
        
        print("\n***************************")
        print('current street ', thisGameActions['Street'], ' your position ', self.position)
        print('your hand ', str(self.hand[0]), str(self.hand[1]))
        print('your stack ', str(nChip))
        print('bet to call ', str(chipsToCall))
        print('current pot', str())
        print('community cards ', thisGameActions['Pot'])
        for i in community_card:
            #print(i.prettyCard())
            print(i)
            
        print('current Street Bet History')
        print(thisGameActions['BetHistory'])
            
        action = input("type in your action: ")
        bet = int(input("type in your bet (int): "))
        print("\n***************************")
        return action, bet